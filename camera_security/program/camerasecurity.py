# camerasecurity.py | camera-security-rpi
# The main class for the program. This class should be created and called from in main
# Author: Lukas Žaromskis
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.authentication.mockauthenticationfacade import MockAuthenticationFacade
from camera_security.communication.iserver import IServer
from camera_security.communication.requestexecutor import RequestExecutor
from camera_security.communication.requests.changepasswordrequest import ChangePasswordRequest
from camera_security.communication.requests.getimagerequest import GetImageRequest
from camera_security.communication.requests.loginrequest import LoginRequest
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.responses.defaultresponses import DefaultResponses
from camera_security.communication.serializers.packetdataserializer import PacketDataSerializer
from camera_security.communication.server import Server
from camera_security.image.imagefacade import ImageFacade
from camera_security.image.processing.resizeboundingboxes import ResizeBoundingBoxes
from camera_security.image.processing.resultfilterbycertainty import ResultFilterByCertainty
from camera_security.image.processing.resultfilterbylabel import ResultFilterByLabel
from camera_security.image.serializers.jpgbase64frameserializer import JpgBase64FrameSerializer
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.program.settings import Settings
from camera_security.utility.consolelogger import ConsoleLogger
from camera_security.utility.exceptions.custombaseexception import CustomBaseException
from camera_security.utility.ilogger import ILogger
from camera_security.utility.loglevel import LogLevel


class CameraSecurity:

    def __init__(self):
        self.__logger: ILogger = None
        self.__auth_facade: AuthenticationFacade = None
        self.__server: IServer = None
        self.__image_facade: ImageFacade = None
        self.__monitoring_facade: MonitoringFacade = None

    def Start(self, settings: Settings):
        self.__logger = ConsoleLogger()
        self.__logger.Log("Initializing...")
        try:
            self.__Initialize(settings)
        except CustomBaseException as e:
            self.__logger.Log("Initialization failed: " + e.message, LogLevel.ERROR)
            self.__logger.Log("Shutting down...")
            return
        self.__logger.Log("Initialization done.")
        self.__logger.Log("To exit press CTRL+C")
        try:
            self.__Run()
        except KeyboardInterrupt:
            self.__logger.Log("Received shutdown signal.")
        except CustomBaseException as e:
            self.__logger.Log("Received unhandled custom exception of type '" + e.__name__ + "': " + e.message, LogLevel.ERROR)
        except Exception as e:
            self.__logger.Log("Received unhandled system exception of type '" + e.__name__ + "'.", LogLevel.ERROR)
        finally:
            # try to send a message to client that the server shut down
            self.__logger.Log("Sending message to client that server is closing...")
            self.__logger.Log("Shutting down...")

    def __Initialize(self, settings: Settings):
        self.__auth_facade = MockAuthenticationFacade()
        self.__image_facade = ImageFacade()
        self.__monitoring_facade = MonitoringFacade("zones.csmz")

        # Setup filters
        self.__image_facade.RegisterFilter(ResultFilterByLabel(["person"]))
        self.__image_facade.RegisterFilter(ResultFilterByCertainty(float(settings.settings_dict[settings.CERTAINTY_THRESHOLD_KEY])))
        self.__image_facade.RegisterFilter(ResizeBoundingBoxes(0.1))

        # Setup executors
        executor = RequestExecutor(PacketDataSerializer(), self.__auth_facade, DefaultResponses())
        executor.RegisterRequest(RequestCode.LOGIN, LoginRequest())
        executor.RegisterRequest(RequestCode.CHANGE_PASSWORD, ChangePasswordRequest())
        executor.RegisterRequest(RequestCode.GET_IMAGE, GetImageRequest(self.__image_facade, JpgBase64FrameSerializer()))

        # Start server
        self.__server = Server("127.0.0.1", 7500, executor, self.__logger)

    def __Run(self):
        self.__server.StartListening()
        while True:
            pass


cs = CameraSecurity()
cs.Start(Settings())

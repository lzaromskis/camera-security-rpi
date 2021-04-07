# camerasecurity.py | camera-security-rpi
# The main class for the program. This class should be created and called from in main
# Author: Lukas Žaromskis
import traceback

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.iserver import IServer
from camera_security.communication.requestexecutor import RequestExecutor
from camera_security.communication.requests.addmonitoredzonerequest import AddMonitoredZoneRequest
from camera_security.communication.requests.changepasswordrequest import ChangePasswordRequest
from camera_security.communication.requests.getallmonitoredzonesrequest import GetAllMonitoredZonesRequest
from camera_security.communication.requests.getimagerequest import GetImageRequest
from camera_security.communication.requests.loginrequest import LoginRequest
from camera_security.communication.requests.removemonitoredzonerequest import RemoveMonitoredZoneRequest
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.requests.setmonitoredzoneactivestaterequest import SetMonitoredZoneActiveStateRequest
from camera_security.communication.responses.defaultresponses import DefaultResponses
from camera_security.communication.serializers.packetdataserializer import PacketDataSerializer
from camera_security.communication.server import Server
from camera_security.image.imagefacade import ImageFacade
from camera_security.image.processing.resizeboundingboxes import ResizeBoundingBoxes
from camera_security.image.processing.resultfilterbycertainty import ResultFilterByCertainty
from camera_security.image.processing.resultfilterbylabel import ResultFilterByLabel
from camera_security.image.serializers.jpgbase64frameserializer import JpgBase64FrameSerializer
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.monitoring.serializers.monitoredzonecollectionserializer import MonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
from camera_security.program.settings import Settings
from camera_security.utility.consolelogger import ConsoleLogger
from camera_security.utility.exceptions.custombaseexception import CustomBaseException
from camera_security.utility.ilogger import ILogger
from camera_security.utility.loglevel import LogLevel
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer


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
            self.__logger.Log("Received unhandled custom exception of type '" + str(type(e)) + "': " + e.message, LogLevel.ERROR)
        except Exception as e:
            self.__logger.Log("Received unhandled system exception of type '" + str(type(e)) + "': " + str(e.args), LogLevel.ERROR)
            self.__logger.Log("Stacktrace: " + traceback.print_exc(), LogLevel.ERROR)
        finally:
            # try to send a message to client that the server shut down
            self.__logger.Log("Sending message to client that server is closing...")
            self.__logger.Log("Shutting down...")

    def __Initialize(self, settings: Settings):
        self.__logger.Log("Creating authentication subsystem...")
        self.__auth_facade = AuthenticationFacade()

        self.__logger.Log("Creating image subsystem...")
        self.__image_facade = ImageFacade(int(settings.settings_dict[settings.CAMERA_ID_KEY]),
                                          settings.settings_dict[settings.TENSOR_MODEL_FILE_KEY],
                                          settings.settings_dict[settings.TENSOR_LABELS_FILE_KEY],
                                          self.__logger)

        self.__logger.Log("Creating monitoring subsystem...")
        self.__monitoring_facade = MonitoringFacade(settings.settings_dict[settings.MONITORED_ZONES_FILENAME_KEY])

        # self.__monitoring_facade.AddZone(MonitoredZone("test_zone", BoundingBox(0, 0, 1, 1)))

        # Setup filters
        self.__logger.Log("Setting up filters...")
        self.__image_facade.RegisterFilter(ResultFilterByLabel(settings.settings_dict[settings.ACCEPTED_LABELS_KEY].split(',')))
        self.__image_facade.RegisterFilter(ResultFilterByCertainty(float(settings.settings_dict[settings.CERTAINTY_THRESHOLD_KEY])))
        self.__image_facade.RegisterFilter(ResizeBoundingBoxes(float(settings.settings_dict[settings.BOUNDS_RESIZE_PERCENTAGE_KEY])))

        # Prepare serializers
        jpg_frame_serializer = JpgBase64FrameSerializer()
        bounds_serializer = BoundingBoxSerializer()
        zone_serializer = MonitoredZoneSerializer(bounds_serializer)
        zones_serializer = MonitoredZoneCollectionSerializer(zone_serializer)

        # Setup executors
        self.__logger.Log("Setting up executors")
        executor = RequestExecutor(PacketDataSerializer(), self.__auth_facade, DefaultResponses())
        executor.RegisterRequest(RequestCode.LOGIN, LoginRequest())
        executor.RegisterRequest(RequestCode.CHANGE_PASSWORD, ChangePasswordRequest())
        executor.RegisterRequest(RequestCode.GET_IMAGE, GetImageRequest(self.__image_facade, jpg_frame_serializer))
        executor.RegisterRequest(RequestCode.GET_ZONES, GetAllMonitoredZonesRequest(self.__monitoring_facade, zones_serializer))
        executor.RegisterRequest(RequestCode.CREATE_ZONE, AddMonitoredZoneRequest(self.__monitoring_facade, zone_serializer))
        executor.RegisterRequest(RequestCode.SET_ZONE_ACTIVITY, SetMonitoredZoneActiveStateRequest(self.__monitoring_facade))
        executor.RegisterRequest(RequestCode.DELETE_ZONE, RemoveMonitoredZoneRequest(self.__monitoring_facade))

        # Create server
        self.__logger.Log("Creating server...")
        self.__server = Server("DELL", 7500, executor, self.__logger)

    def __Run(self):
        self.__server.StartListening()
        while True:
            detected = self.__image_facade.ProcessFrame()
            collisions = self.__monitoring_facade.GetCollidingZones(detected)
            print(len(collisions))

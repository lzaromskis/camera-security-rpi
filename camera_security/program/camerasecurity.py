# camerasecurity.py | camera-security-rpi
# The main class for the program. This class should be created and called from in main
# Author: Lukas Žaromskis
import traceback
from datetime import datetime
from socket import gethostname
from time import sleep
from typing import List

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.alertserver import AlertServer
from camera_security.communication.alertservertls import AlertServerTLS
from camera_security.communication.ialertserver import IAlertServer
from camera_security.communication.iserver import IServer
from camera_security.communication.requestexecutor import RequestExecutor
from camera_security.communication.requests.addmonitoredzonerequest import AddMonitoredZoneRequest
from camera_security.communication.requests.changepasswordrequest import ChangePasswordRequest
from camera_security.communication.requests.getalertimagerequest import GetAlertImageRequest
from camera_security.communication.requests.getallmonitoredzonesrequest import GetAllMonitoredZonesRequest
from camera_security.communication.requests.getimagerequest import GetImageRequest
from camera_security.communication.requests.getlatestalertsrequest import GetLatestAlertsRequest
from camera_security.communication.requests.loginrequest import LoginRequest
from camera_security.communication.requests.removemonitoredzonerequest import RemoveMonitoredZoneRequest
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.requests.setmonitoredzoneactivestaterequest import SetMonitoredZoneActiveStateRequest
from camera_security.communication.responses.defaultresponses import DefaultResponses
from camera_security.communication.serializers.packetdataserializer import PacketDataSerializer
from camera_security.communication.server import Server
from camera_security.communication.servertls import ServerTLS
from camera_security.communication.websocketmessages import WebsocketMessages
from camera_security.image.imagedrawer import ImageDrawer
from camera_security.image.imagefacade import ImageFacade
from camera_security.image.processing.resizeboundingboxes import ResizeBoundingBoxes
from camera_security.image.processing.resultfilterbycertainty import ResultFilterByCertainty
from camera_security.image.processing.resultfilterbylabel import ResultFilterByLabel
from camera_security.image.serializers.jpgbase64frameserializer import JpgBase64FrameSerializer
from camera_security.monitoring.alerts.alertsfacade import AlertsFacade
from camera_security.monitoring.alerts.ialertaction import IAlertAction
from camera_security.monitoring.alerts.savealertaction import SaveAlertAction
from camera_security.monitoring.alerts.serveralertaction import ServerAlertAction
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.monitoring.serializers.monitoredzonecollectionserializer import MonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
from camera_security.program.settings import Settings
from camera_security.utility.consolelogger import ConsoleLogger
from camera_security.utility.exceptions.custombaseexception import CustomBaseException
from camera_security.utility.ilogger import ILogger
from camera_security.utility.loglevel import LogLevel
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer
from camera_security.utility.serializers.stringlistserializer import StringListSerializer


class CameraSecurity:

    def __init__(self):
        self.__logger: ILogger = None
        self.__auth_facade: AuthenticationFacade = None
        self.__server: IServer = None
        self.__alert_server: IAlertServer = None
        self.__image_facade: ImageFacade = None
        self.__monitoring_facade: MonitoringFacade = None
        self.__alerts_facade: AlertsFacade = None
        self.__alert_actions: List[IAlertAction] = list()

        # variables for processing steps
        self.__timeout = 30
        self.__detection_count = 0
        self.__detection_threshold = 2
        self.__previous_detection_state = False
        self.__previous_saved_detection_time = datetime.utcnow()

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
            self.__alert_server.SendMessage(WebsocketMessages.CLOSE)
            sleep(2)
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

        self.__logger.Log("Creating alerts subsystem...")
        self.__alerts_facade = AlertsFacade(settings.settings_dict[settings.ALERTS_FOLDER_KEY],
                                            int(settings.settings_dict[settings.ALERTS_TO_KEEP_KEY]))

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
        string_list_serializer = StringListSerializer()

        # Prepare others
        image_drawer = ImageDrawer()

        # Setup executors
        self.__logger.Log("Setting up executors...")
        executor = RequestExecutor(PacketDataSerializer(), self.__auth_facade, DefaultResponses())
        executor.RegisterRequest(RequestCode.LOGIN, LoginRequest())
        executor.RegisterRequest(RequestCode.CHANGE_PASSWORD, ChangePasswordRequest())
        executor.RegisterRequest(RequestCode.GET_IMAGE, GetImageRequest(self.__image_facade, self.__monitoring_facade, image_drawer, jpg_frame_serializer))
        executor.RegisterRequest(RequestCode.GET_ZONES, GetAllMonitoredZonesRequest(self.__monitoring_facade, zones_serializer))
        executor.RegisterRequest(RequestCode.CREATE_ZONE, AddMonitoredZoneRequest(self.__monitoring_facade, zone_serializer))
        executor.RegisterRequest(RequestCode.SET_ZONE_ACTIVITY, SetMonitoredZoneActiveStateRequest(self.__monitoring_facade))
        executor.RegisterRequest(RequestCode.DELETE_ZONE, RemoveMonitoredZoneRequest(self.__monitoring_facade))
        executor.RegisterRequest(RequestCode.GET_ALERT_LIST, GetLatestAlertsRequest(self.__alerts_facade, string_list_serializer))
        executor.RegisterRequest(RequestCode.GET_ALERT_IMAGE, GetAlertImageRequest(self.__alerts_facade, jpg_frame_serializer))

        # Create servers
        self.__logger.Log("Creating servers...")
        if settings.settings_dict[settings.USE_TLS_KEY] == "true":
            self.__logger.Log("Using TLS for server...")
            cert_file = settings.settings_dict[settings.CERT_FILE_KEY]
            key_file = settings.settings_dict[settings.KEY_FILE_KEY]
            self.__server = ServerTLS("127.0.0.1", 7500, cert_file, key_file, executor, self.__logger)
            self.__alert_server = AlertServerTLS("127.0.0.1", 7501, cert_file, key_file, self.__logger)
            # self.__server = ServerTLS(gethostname(), 7500, cert_file, key_file, executor, self.__logger)
            # self.__alert_server = AlertServerTLS(gethostname(), 7501, cert_file, key_file, self.__logger)
        else:
            self.__server = Server("127.0.0.1", 7500, executor, self.__logger)
            self.__alert_server = AlertServer("127.0.0.1", 7501, self.__logger)
            #self.__server = Server(gethostname(), 7500, executor, self.__logger)
            # self.__alert_server = AlertServer(gethostname(), 7501, self.__auth_facade)

        # Setup alert actions
        self.__logger.Log("Setting up alert actions...")
        self.__alert_actions.append(SaveAlertAction(self.__alerts_facade))
        self.__alert_actions.append(ServerAlertAction(self.__alert_server))

    def __Run(self):
        self.__server.StartListening()
        self.__alert_server.StartListening()
        while True:
            self.__ProcessStep()

    def __ProcessStep(self):
        if self.__monitoring_facade.GetActiveZoneCount() == 0:
            self.__image_facade.RefreshFrame()
            return
        detections = self.__image_facade.ProcessFrame()
        collisions = self.__monitoring_facade.GetCollidingZones(detections)
        detection_state = len(collisions) != 0
        if self.__previous_detection_state == detection_state:
            self.__detection_count = self.__detection_count + 1
        else:
            self.__detection_count = 1
            self.__previous_detection_state = detection_state
        if detection_state and self.__detection_count >= self.__detection_threshold:
            current_time = datetime.utcnow()
            delta_time = current_time - self.__previous_saved_detection_time
            if delta_time.total_seconds() > self.__timeout:
                for zone in collisions:
                    self.__logger.Log(''.join(["Detected object in zone '", zone.GetName(), "'!"]))
                self.__previous_saved_detection_time = current_time
                image_obj = self.__image_facade.GetFrame()
                alert_data = dict(image=image_obj)
                for action in self.__alert_actions:
                    action.Execute(**alert_data)
                # self.__alerts_facade.SaveAlert(image)
                # self.__alert_server.SendMessage(WebsocketMessages.ALERT)

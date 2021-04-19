# alertserver.py | camera-security-rpi
# Describes the AlertServer class implementing the IAlertServer interface
# Author: Lukas Žaromskis
import threading

from simple_websocket_server import WebSocketServer

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.alertwebsocket import AlertWebsocket, send_message_to_websocket
from camera_security.communication.ialertserver import IAlertServer
from camera_security.utility.ilogger import ILogger


class AlertServer(IAlertServer):

    def __init__(self, host: str, port: int, logger: ILogger):
        self.__logger = logger
        self.__host = host
        self.__port = port
        AlertWebsocket.GLOBAL_LOGGER = logger
        self.__thread = None
        self.__server = None

    def StartListening(self):
        self.__thread = threading.Thread(target=self.__StartListeningTask)
        # Set thread as daemon so it closes with the main thread
        self.__thread.daemon = True
        self.__thread.start()

    def SendMessage(self, message: str):
        send_message_to_websocket(message)

    def __StartListeningTask(self):
        self.__logger.Log("Opening websocket " + str(self.__host) + ":" + str(self.__port))
        self.__server = WebSocketServer(self.__host, self.__port, AlertWebsocket)
        self.__server.serve_forever()

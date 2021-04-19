# alertservertls.py | camera-security-rpi
# Describes the AlertServer class implementing the IAlertServer interface
# Author: Lukas Žaromskis
import ssl
import threading

from simple_websocket_server import WebSocketServer

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.alertwebsocket import AlertWebsocket, send_message_to_websocket
from camera_security.communication.ialertserver import IAlertServer
from camera_security.utility.ilogger import ILogger


class AlertServerTLS(IAlertServer):

    def __init__(self, host: str, port: int, cert_file: str, key_file: str, logger: ILogger):
        self.__logger = logger
        self.__host = host
        self.__port = port
        self.__cert_file = cert_file
        self.__key_file = key_file
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
        self.__server = WebSocketServer(self.__host, self.__port, AlertWebsocket, self.__cert_file, self.__key_file, ssl.PROTOCOL_TLSv1)
        self.__server.serve_forever()

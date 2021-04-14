# ialertserver.py | camera-security-rpi
# Describes the AlertWebsocket class for handling websocket communications
# Author: Lukas Žaromskis

from simple_websocket_server import WebSocket
from camera_security.communication.websocketmessages import WebsocketMessages
from camera_security.utility.ilogger import ILogger


def send_message_to_websocket(message: str):
    if AlertWebsocket.GLOBAL_WEBSOCKET is not None:
        AlertWebsocket.GLOBAL_WEBSOCKET.send_message(message)
        if AlertWebsocket.GLOBAL_LOGGER is not None:
            AlertWebsocket.GLOBAL_LOGGER.Log("Sending message to " + str(AlertWebsocket.GLOBAL_WEBSOCKET.address[0]))
    else:
        if AlertWebsocket.GLOBAL_LOGGER is not None:
            AlertWebsocket.GLOBAL_LOGGER.Log("Cannot send message because websocket is closed")

class AlertWebsocket(WebSocket):
    GLOBAL_WEBSOCKET: WebSocket = None
    GLOBAL_LOGGER: ILogger = None

    def handle(self):
        if AlertWebsocket.GLOBAL_LOGGER is not None:
            AlertWebsocket.GLOBAL_LOGGER.Log("Websocket received message from " + str(self.address[0]))
        data = self.data
        str_data = data
        if str_data == WebsocketMessages.PING:
            self.send_message(WebsocketMessages.PONG)

    def connected(self):
        if AlertWebsocket.GLOBAL_WEBSOCKET is not None:
            return
        AlertWebsocket.GLOBAL_WEBSOCKET = self
        if AlertWebsocket.GLOBAL_LOGGER is not None:
            AlertWebsocket.GLOBAL_LOGGER.Log("Websocket connected to " + str(self.address[0]))

    def handle_close(self):
        AlertWebsocket.GLOBAL_WEBSOCKET = None
        if AlertWebsocket.GLOBAL_LOGGER is not None:
            AlertWebsocket.GLOBAL_LOGGER.Log("Websocket disconnected from " + str(self.address[0]))

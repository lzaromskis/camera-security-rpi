# serveralertaction.py | camera-security-rpi
# Implements the IAlertAction interface for alerting the client using IAlertServer
# Author: Lukas Žaromskis
from camera_security.communication.ialertserver import IAlertServer
from camera_security.communication.websocketmessages import WebsocketMessages
from camera_security.monitoring.alerts.ialertaction import IAlertAction


class ServerAlertAction(IAlertAction):

    def __init__(self, alert_server: IAlertServer):
        self.__alert_server = alert_server

    def Execute(self, **kwargs):
        self.__alert_server.SendMessage(WebsocketMessages.ALERT)

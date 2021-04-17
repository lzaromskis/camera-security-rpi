# savealertaction.py | camera-security-rpi
# Implements the IAlertAction interface for saving the alert to disk
# Author: Lukas Žaromskis

from camera_security.image.frame import Frame
from camera_security.monitoring.alerts.alertsfacade import AlertsFacade
from camera_security.monitoring.alerts.ialertaction import IAlertAction


class SaveAlertAction(IAlertAction):

    def __init__(self, alerts_facade: AlertsFacade):
        self.__alerts_facade = alerts_facade

    def Execute(self, **kwargs):
        image = kwargs["image"]
        if image is None or type(image) != Frame:
            raise ValueError("Required attribute 'image' is not found or invalid")
        self.__alerts_facade.SaveAlert(image)

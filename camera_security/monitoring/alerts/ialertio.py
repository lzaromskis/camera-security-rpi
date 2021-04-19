# ialertio.py | camera-security-rpi
# Describes the IAlertIO interface for reading and saving testalerts to disk
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import List

from camera_security.monitoring.alerts.alertdata import AlertData


class IAlertIO(ABC):

    @abstractmethod
    def SaveAlert(self, alert: AlertData):
        """
        Saves the alert to disk
        """
        raise NotImplementedError()

    @abstractmethod
    def GetAlert(self, timestamp: str) -> AlertData:
        """
        Reads and returns the alert to disk
        """
        raise NotImplementedError()

    @abstractmethod
    def GetAvailableAlerts(self) -> List[str]:
        """
        Gets all available testalerts
        """
        raise NotImplementedError()

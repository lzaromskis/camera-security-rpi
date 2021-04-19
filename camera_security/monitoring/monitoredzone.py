# monitoredzone.py | camera-security-rpi
# Describes the MonitoredZone class for storing information about a monitored zone
# Author: Lukas Žaromskis
from typing import List

from camera_security.utility.boundingbox import BoundingBox


class MonitoredZone:

    def __init__(self, name: str, bounds: BoundingBox, labels: List[str]):
        self.__name = name
        self.__bounds = bounds
        self.__active = False
        self.__labels = labels

    def GetName(self) -> str:
        """
        Returns the name of the monitored zone
        """
        return self.__name

    def GetBounds(self) -> BoundingBox:
        """
        Returns the bounds of the monitored zone
        """
        return self.__bounds

    def GetLabels(self) -> List[str]:
        """
        Returns the labels that can trigger the zone
        """
        return self.__labels

    def IsActive(self) -> bool:
        """
        Returns true if the monitored zone is active
        """
        return self.__active

    def SetActive(self, active: bool):
        """
        Sets the active state of the monitored zone
        """
        self.__active = active

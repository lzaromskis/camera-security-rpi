# imonitoredzonecollectionio.py | camera-security-rpi
# Describes the IMonitoredZoneCollectionIO interface for reading and writing monitored zone collection data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection


class IMonitoredZoneCollectionIO(ABC):

    @abstractmethod
    def GetMonitoredZones(self, filename: str) -> MonitoredZoneCollection:
        """
        Returns a monitored zone collection from the given file
        """
        raise NotImplementedError()

    @abstractmethod
    def SaveMonitoredZones(self, zones: MonitoredZoneCollection, filename: str):
        """
        Saves the given monitored zones to the given file:
        """
        raise NotImplementedError()

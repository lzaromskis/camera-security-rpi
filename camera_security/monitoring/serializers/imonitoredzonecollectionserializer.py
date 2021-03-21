# imonitoredzonecollectionserializer.py | camera-security-rpi
# Describes the IMonitoredZoneCollectionSerializer interface for serializing monitored zone collections
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection


class IMonitoredZoneCollectionSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: MonitoredZoneCollection) -> str:
        """
        Serializes the given monitored zone collection to a string.
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> MonitoredZoneCollection:
        """
        Deserializes the given string to a monitored zone collection
        """
        raise NotImplementedError()

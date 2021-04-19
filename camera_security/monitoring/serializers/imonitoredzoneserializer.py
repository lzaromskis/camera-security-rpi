# imonitoredzoneserializer.py | camera-security-rpi
# Describes the IMonitoredZoneSerializer interface for serializing monitored zones
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.monitoring.monitoredzone import MonitoredZone


class IMonitoredZoneSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: MonitoredZone) -> str:
        """
        Serializes the given monitored zone to a string
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> MonitoredZone:
        """
        Deserializes the given string to a monitored zone
        """
        raise NotImplementedError()

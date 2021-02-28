# ipacketdataserializer.py | camera-security-rpi
# Describes the interface for packet data serialization
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IPacketDataSerializer(ABC):

    @abstractmethod
    def Serialize(self, data):
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data):
        raise NotImplementedError()

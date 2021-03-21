# ipacketdataserializer.py | camera-security-rpi
# Describes the interface for packet data serialization
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

from camera_security.communication.packetdata import PacketData


class IPacketDataSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: PacketData) -> str:
        """
        Serializes the PacketData object to a string
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> PacketData:
        """
        Deserializes a string to a PacketData object
        """
        raise NotImplementedError()

# iframeserializer.py | camera-security-rpi
# Describes the IFrameSerializer interface for serializing frames into strings
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

from camera_security.image.frame import Frame


class IFrameSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: Frame) -> str:
        """
        Serializes the given frame to a string
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> Frame:
        """
        Constructs a frame from the serialized data
        """
        raise NotImplementedError()

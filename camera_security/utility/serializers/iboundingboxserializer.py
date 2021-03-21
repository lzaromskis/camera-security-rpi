# iboundingboxserializer.py | camera-security-rpi
# Describes the IBoundingBoxSerializer interface for serializing bounding boxes
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.utility.boundingbox import BoundingBox


class IBoundingBoxSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: BoundingBox) -> str:
        """
        Serializes the given bounding box to a string
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> BoundingBox:
        """
        Deserializes the given string to a bounding box
        """
        raise NotImplementedError()

# istringlistserializer.py | camera-security-rpi
# Describes the IStringListSerializer interface for serializing string lists
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import List


class IStringListSerializer(ABC):

    @abstractmethod
    def Serialize(self, data: List[str]) -> str:
        """
        Serializes the given string list to a string
        """
        raise NotImplementedError()

    @abstractmethod
    def Deserialize(self, data: str) -> List[str]:
        """
        Deserializes the given string to a string list
        """
        raise NotImplementedError()

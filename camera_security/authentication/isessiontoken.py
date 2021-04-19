# isessiontoken.py | camera-security-rpi
# Describes the ISessionToken interface for session data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class ISessionToken(ABC):

    @abstractmethod
    def IsValid(self, secret: str) -> bool:
        """
        Checks if the secret is valid.
        """
        raise NotImplementedError()

    @abstractmethod
    def GetSecret(self) -> str:
        """
        Gets the secret.
        """
        raise NotImplementedError()

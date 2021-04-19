# ipasswordio.py | camera-security-rpi
# Describes the IPasswordIO interface for reading and writing password data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.authentication.passworddata import PasswordData


class IPasswordIO(ABC):

    @abstractmethod
    def GetPassword(self) -> PasswordData:
        """
        Gets the password data: hash and salt.
        """
        raise NotImplementedError()

    @abstractmethod
    def SavePassword(self, new_data: PasswordData):
        """
        Saves a new password.
        """
        raise NotImplementedError()

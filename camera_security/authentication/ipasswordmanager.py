# ipasswordmanager.py | camera-security-rpi
# Describes the IPasswordManager interface for managing password tasks
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IPasswordManager(ABC):

    @abstractmethod
    def IsValid(self, password: str) -> bool:
        """
        Checks if the password is valid.
        """
        raise NotImplementedError()

    @abstractmethod
    def ChangePassword(self, new_password: str):
        """
        Changes the password into the new given password.
        """
        raise NotImplementedError()


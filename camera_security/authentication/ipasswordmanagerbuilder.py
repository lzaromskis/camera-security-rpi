# ipasswordmanagerbuilder.py | camera-security-rpi
# Describes the IPasswordManagerFactory interface for creating a password manager
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.authentication.ipasswordmanager import IPasswordManager


class IPasswordManagerBuilder(ABC):

    @abstractmethod
    def AddSecretGenerator(self, gen_method: str) -> 'IPasswordManagerBuilder':
        """
        Adds a specified secret generator.
        """
        raise NotImplementedError()

    @abstractmethod
    def AddPasswordIO(self, io_method: str, password_file: str) -> 'IPasswordManagerBuilder':
        """
        Adds a specified password io.
        """
        raise NotImplementedError()

    @abstractmethod
    def AddHash(self, hash_method: str) -> 'IPasswordManagerBuilder':
        """
        Adds a specified hash method.
        """

    @abstractmethod
    def Build(self) -> IPasswordManager:
        """
        Builds a PasswordManager based on the specified methods. Default value is chosen if no method specified.
        """
        raise NotImplementedError()

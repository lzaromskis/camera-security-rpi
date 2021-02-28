# ipasswordmanager.py | camera-security-rpi
# Describes the IPasswordManager interface for managing password tasks
# Implements the interface with PasswordManager class
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.authentication.passworddata import PasswordData


class IPasswordManager(ABC):

    @abstractmethod
    def IsValid(self, password: str) -> bool:
        """
        Checks if the password is valid
        """
        raise NotImplementedError()

    @abstractmethod
    def ChangePassword(self, new_password: str):
        """
        Changes the password into the new given password
        """
        raise NotImplementedError()


class PasswordManager(IPasswordManager):

    def __init__(self, hash, password_io, salt):
        self.hash = hash
        self.passwordIO = password_io
        self.salt = salt

    def IsValid(self, password):
        data = self.passwordIO.GetPassword()
        calculated_hash = self.hash.Hash(password, data.salt)
        return calculated_hash == data.hash

    def ChangePassword(self, new_password):
        generated_salt = self.salt.Generate(16)
        calculated_hash = self.hash.Hash(new_password, generated_salt)
        self.passwordIO.SavePassword(PasswordData(calculated_hash, generated_salt))


# ipasswordmanagerfactory.py | camera-security-rpi
# Describes the IPasswordManagerFactory interface for creating a password manager
# Implements the interface with PasswordManagerFactory class
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.authentication.ihash import HashSHA256
from camera_security.authentication.ipassword_io import PasswordIO
from camera_security.authentication.isecretgenerator import SecretGenerator
from camera_security.authentication.ipasswordmanager import PasswordManager


class IPasswordManagerFactory(ABC):

    @abstractmethod
    def GetManager(self):
        raise NotImplementedError()


class PasswordManagerFactory(IPasswordManagerFactory):

    def __init__(self):
        pass

    def GetManager(self):
        return PasswordManager(HashSHA256(), PasswordIO("password"), SecretGenerator())

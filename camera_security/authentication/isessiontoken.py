# isessiontoken.py | camera-security-rpi
# Describes the ISessionToken interface for session data
# Implements the interface with SessionTokenClass
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta


class ISessionToken(ABC):

    @abstractmethod
    def IsValid(self, secret):
        raise NotImplementedError()

    @abstractmethod
    def GetSecret(self):
        raise NotImplementedError()


class SessionToken(ISessionToken):

    def __init__(self, secret_generator):
        self.secret = secret_generator.Generate(32)
        self.expirationDate = datetime.now() + timedelta(hours=6)

    def IsValid(self, secret):
        return secret == self.secret and datetime.now() < self.expirationDate

    def GetSecret(self):
        return self.secret

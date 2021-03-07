# sessiontoken.py | camera-security-rpi
# Implements the ISessionToken interface with SessionToken class
# Author: Lukas Žaromskis

from datetime import datetime, timedelta

from camera_security.authentication.isecretgenerator import ISecretGenerator
from camera_security.authentication.isessiontoken import ISessionToken


class SessionToken(ISessionToken):

    def __init__(self, secret_generator: ISecretGenerator):
        self.__secret = secret_generator.Generate(32)
        self.__expirationDate = datetime.now() + timedelta(hours=6)

    def IsValid(self, secret: str) -> bool:
        return secret == self.__secret and datetime.now() < self.__expirationDate

    def GetSecret(self) -> str:
        return self.__secret

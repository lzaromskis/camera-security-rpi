# authenticationfacade.py | camera-security-rpi
# Implements the SessionManager class for managing a session with the user
# Author: Lukas Žaromskis

from camera_security.authentication.ipasswordmanagerfactory import PasswordManagerFactory
from camera_security.authentication.isessiontoken import SessionToken
from camera_security.authentication.isecretgenerator import SecretGenerator
from camera_security.authentication.isessiontoken import ISessionToken


class AuthenticationFacade:

    def __init__(self):
        factory = PasswordManagerFactory()
        self.__passwordManager = factory.GetManager()
        self.__token = None

    def IsAuthenticated(self, secret: str):
        """
        Checks if the user is already authenticated
        """
        return self.__token is not None and self.__token.IsValid(secret)

    def Authenticate(self, password: str) -> str:
        """
        Tries to authenticate the user.\n
        :return: ISessionToken if authentication successful or None if authentication failed
        """
        if self.__passwordManager.IsValid(password):
            self.__token = SessionToken(SecretGenerator())
            return self.__token.GetSecret()
        else:
            return None

    def ChangePassword(self, new_password: str):
        """
        Changes the password
        """
        self.__passwordManager.ChangePassword(new_password)

    def IsPasswordValid(self, password: str) -> bool:
        """
        Checks if the given password is valid
        """
        return self.__passwordManager.IsValid(password)
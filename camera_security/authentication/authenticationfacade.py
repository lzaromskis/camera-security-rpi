# authenticationfacade.py | camera-security-rpi
# Implements the SessionManager class for managing a session with the user
# Author: Lukas Žaromskis

from typing import Optional
from camera_security.authentication.passwordmanagerbuilder import PasswordManagerBuilder
from camera_security.authentication.sessiontoken import SessionToken
from camera_security.authentication.secretgenerator import SecretGenerator


class AuthenticationFacade:

    def __init__(self):
        factory = PasswordManagerBuilder()
        self.__passwordManager = factory.AddPasswordIO("passwordio", "password.cspw").Build()
        self.__token = None

    def IsAuthenticated(self, secret: str) -> bool:
        """
        Checks if the user is already authenticated.
        """
        return self.__token is not None and self.__token.IsValid(secret)

    def Authenticate(self, password: str) -> Optional[str]:
        """
        Tries to authenticate the user. Returns None if failed to authenticate.
        """
        if self.__passwordManager.IsValid(password):
            self.__token = SessionToken(SecretGenerator())
            return self.__token.GetSecret()
        else:
            return None

    def ChangePassword(self, new_password: str):
        """
        Changes the password.
        """
        self.__passwordManager.ChangePassword(new_password)

    def IsPasswordValid(self, password: str) -> bool:
        """
        Checks if the given password is valid.
        """
        return self.__passwordManager.IsValid(password)

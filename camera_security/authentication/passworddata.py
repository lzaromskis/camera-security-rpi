# passworddata.py | camera-security-rpi
# Implements the class for storing password data: hash and salt
# Author: Lukas Žaromskis

class PasswordData:
    def __init__(self, hash: str, salt: str):
        self.__hash = hash
        self.__salt = salt

    def GetHash(self) -> str:
        """
        Gets the hash of the password.
        """
        return self.__hash

    def GetSalt(self) -> str:
        """
        Gets the salt of the password.
        """
        return self.__salt

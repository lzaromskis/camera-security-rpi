# ipasswordio.py | camera-security-rpi
# Describes the IPasswordIO interface for reading and writing password data
# Implements the interface with PasswordIO class
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from os import path
from camera_security.authentication.passworddata import PasswordData
from camera_security.exceptions import InvalidFileError
from camera_security.exceptions import FileNotFoundError


class IPasswordIO(ABC):

    @abstractmethod
    def GetPassword(self) -> PasswordData:
        """
        Gets the password data: hash and salt
        """
        raise NotImplementedError()

    @abstractmethod
    def SavePassword(self, new_data: PasswordData):
        """
        Saves a new password
        """
        raise NotImplementedError()


MAGIC = "CSpw"


class PasswordIO(IPasswordIO):

    def __init__(self, location):
        self.location = location

    def GetPassword(self):
        if not path.isfile(self.location):
            raise FileNotFoundError("File \"" + self.location + "\" does not exist!")
        f = open(self.location, "r")
        raw_data = f.readline()
        if not raw_data.startswith(MAGIC):
            f.close()
            raise InvalidFileError("File \"" + self.location + "\" is not a valid password file!")
        split_data = raw_data.split("|")
        if len(split_data) != 3:
            f.close()
            raise InvalidFileError(
                "File \"" + self.location + "\" must contain only 3 data attributes: magic number, hash and salt!")
        ret_val = PasswordData(split_data[1], split_data[2])
        f.close()
        return ret_val

    def SavePassword(self, new_data):
        f = open(self.location, "w")
        f.write(MAGIC + "|" + new_data.hash + "|" + new_data.salt)
        f.close()

# passwordio.py | camera-security-rpi
# Implements the IPasswordIO interface with PasswordIO class
# Author: Lukas Žaromskis

from os import path
from camera_security.authentication.ipasswordio import IPasswordIO
from camera_security.authentication.passworddata import PasswordData
from camera_security.utility.exceptions.invalidfileerror import InvalidFileError
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class PasswordIO(IPasswordIO):

    MAGIC = "CSpw"

    def __init__(self, location: str):
        self.__location = location

    def GetPassword(self) -> PasswordData:
        if not path.isfile(self.__location):
            raise FileNotFoundError("File \"" + self.__location + "\" does not exist!")
        f = open(self.__location, "r")
        raw_data = f.readline()
        if not raw_data.startswith(self.MAGIC):
            f.close()
            raise InvalidFileError("File \"" + self.__location + "\" is not a valid password file!")
        split_data = raw_data.split("|")
        if len(split_data) != 3:
            f.close()
            raise InvalidFileError(
                "File \"" + self.__location + "\" must contain only 3 data attributes: magic number, hash and salt!")
        ret_val = PasswordData(split_data[1].strip(), split_data[2].strip())
        f.close()
        return ret_val

    def SavePassword(self, new_data: PasswordData):
        f = open(self.__location, "w")
        f.write(''.join([self.MAGIC, "|", new_data.GetHash(), "|", new_data.GetSalt()]))
        f.close()

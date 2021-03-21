# invalidfileerror.py | camera-security-rpi
# Describes the InvalidFileError exception which is thrown when a given file is in an incorrect format
# Author: Lukas Žaromskis

from camera_security.utility.exceptions.custombaseexception import CustomBaseException


class InvalidFileError(CustomBaseException):

    def __init__(self, message: str):
        super().__init__(message)

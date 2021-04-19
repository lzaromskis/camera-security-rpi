# filenotfounderror.py | camera-security-rpi
# Describes the FileNotFoundError exception which is thrown when a given file is not found
# Author: Lukas Žaromskis

from camera_security.utility.exceptions.custombaseexception import CustomBaseException


class FileNotFoundError(CustomBaseException):

    def __init__(self, message: str):
        super().__init__(message)

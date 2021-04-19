# requestnotfounderror.py | camera-security-rpi
# Describes the RequestNotFound exception which is thrown when a given request does not exist
# Author: Lukas Žaromskis

from camera_security.utility.exceptions.custombaseexception import CustomBaseException


class RequestNotFoundError(CustomBaseException):

    def __init__(self, message: str, response: str):
        super().__init__(message)
        self.response = response

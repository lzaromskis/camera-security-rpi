# deserializationfailederror.py | camera-security-rpi
# Describes the DeserializationFailedError exception which is thrown when an error occurs during the deserialization process
# Author: Lukas Žaromskis

from camera_security.utility.exceptions.custombaseexception import CustomBaseException


class DeserializationFailedError(CustomBaseException):

    def __init__(self, message: str):
        super().__init__(message)

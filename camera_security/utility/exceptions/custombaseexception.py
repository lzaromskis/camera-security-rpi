# custombaseexception.py | camera-security-rpi
# Describes the base for custom exceptions
# Author: Lukas Žaromskis


class CustomBaseException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

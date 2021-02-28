# exceptions.py | camera-security-rpi
# Describes custom exceptions
# Author: Lukas Žaromskis

class InvalidFileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FileNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RequestNotFoundError(Exception):
    def __init__(self, message: str, response: str):
        self.message = message
        self.response = response
        super().__init__(self.message)

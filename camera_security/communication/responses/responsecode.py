# responsecode.py | camera-security-rpi
# Describes the response codes the server can send
# Author: Lukas Žaromskis

from enum import Enum


class ResponseCode(Enum):
    OK = 10
    NOT_AUTHENTICATED = 20
    INVALID_PACKET = 30
    BAD_PASSWORD = 40
    INVALID_REQUEST = 50

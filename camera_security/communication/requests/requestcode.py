# requestcode.py | camera-security-rpi
# Describes the request codes the client can send
# Author: Lukas Žaromskis

from enum import Enum


class RequestCode(Enum):
    LOGIN = 15
    CHANGE_PASSWORD = 25
    GET_IMAGE = 35
    SET_ZONE_INIT = 45

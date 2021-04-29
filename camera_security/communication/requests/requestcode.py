# requestcode.py | camera-security-rpi
# Describes the request codes the client can send
# Author: Lukas Žaromskis

from enum import Enum


class RequestCode(Enum):
    LOGIN = 15
    CHANGE_PASSWORD = 25
    GET_IMAGE = 35
    GET_ZONES = 45
    CREATE_ZONE = 55
    SET_ZONE_ACTIVITY = 65
    DELETE_ZONE = 75
    GET_ALERT_LIST = 85
    GET_ALERT_IMAGE = 95
    CREATE_ZONE_INIT = 105


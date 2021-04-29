# requestcode.py | camera-security-rpi
# Describes the request codes the client can send
# Author: Lukas Žaromskis

from enum import Enum


class RequestCode(Enum):
    LOGIN = 15
    CHANGE_PASSWORD = 25
    GET_IMAGE = 35
<<<<<<< HEAD
    GET_ZONES = 45
    CREATE_ZONE = 55
    SET_ZONE_ACTIVITY = 65
    DELETE_ZONE = 75
    GET_ALERT_LIST = 85
    GET_ALERT_IMAGE = 95
    CREATE_ZONE_INIT = 105
=======
    GET_IMAGE_RAW = 45
    GET_ZONES = 55
    CREATE_ZONE = 65
    SET_ZONE_ACTIVITY = 75
    DELETE_ZONE = 85
    GET_ALERT_LIST = 95
    GET_ALERT_IMAGE = 105
    GET_HEATMAP = 115
    CREATE_ZONE_INIT = 125
>>>>>>> main


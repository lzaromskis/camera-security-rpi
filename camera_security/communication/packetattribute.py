# packetattribute.py | camera-security-rpi
# Describes the attributes the packet can have
# Author: Lukas Žaromskis

from enum import Enum


class PacketAttribute:
    CODE = "code"
    PASSWORD = "password"
    PASSWORD_NEW = "password_new"
    SECRET = "secret"
    IMAGE = "image"
    MESSAGE = "message"
    ZONES = "monitored_zones"
    ZONE = "zone"
    ZONE_NAME = "zone_name"
    ZONE_ACTIVE = "zone_active"

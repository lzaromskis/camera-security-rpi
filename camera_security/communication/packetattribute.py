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

#    def __str__(self):
#        return self.value

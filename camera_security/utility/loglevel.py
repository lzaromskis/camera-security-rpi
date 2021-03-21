# loglevel.py | camera-security-rpi
# Describes the log levels
# Author: Lukas Žaromskis

from enum import Enum


class LogLevel(Enum):
    NONE = 0
    INFORMATION = 1
    WARNING = 2
    ERROR = 3

# ilogger.py | camera-security-rpi
# Describes the ILogger interface for logging
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

from camera_security.utility.loglevel import LogLevel


class ILogger(ABC):

    @abstractmethod
<<<<<<< HEAD
    def Log(self, message: str, level: LogLevel = LogLevel.INFO):
=======
    def Log(self, message: str, level: LogLevel = LogLevel.NONE):
>>>>>>> main
        """
        Logs message
        """
        raise NotImplementedError()

# ilogger.py | camera-security-rpi
# Describes the ILogger interface for logging
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class ILogger(ABC):

    @abstractmethod
    def Log(self, message: str):
        """
        Logs message
        """
        raise NotImplementedError()
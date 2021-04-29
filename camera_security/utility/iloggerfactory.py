# iloggerfactory.py | camera-security-rpi
# Describes the ILoggerFactory interface for creating loggers
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

from camera_security.utility.ilogger import ILogger


class ILoggerFactory(ABC):

    @abstractmethod
    def GetLogger(self, logger_type: str) -> ILogger:
        """
        Returns a logger of given type.
        If no logger of given type exists, a regular console logger is returned.
        """
        raise NotImplementedError()

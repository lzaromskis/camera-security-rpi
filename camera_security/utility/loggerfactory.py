# loggerfactory.py | camera-security-rpi
# Implements the ILoggerFactory interface for creating loggers
# Author: Lukas Žaromskis

from camera_security.utility.consolelogger import ConsoleLogger
from camera_security.utility.filelogger import FileLogger
from camera_security.utility.ilogger import ILogger
from camera_security.utility.iloggerfactory import ILoggerFactory


class LoggerFactory(ILoggerFactory):
    def GetLogger(self, logger_type: str, **kwargs) -> ILogger:
        if logger_type == "console":
            return ConsoleLogger()
        elif logger_type == "file":
            return FileLogger(kwargs["file"], kwargs["append"].lower() == "true")
        else:
            return ConsoleLogger()

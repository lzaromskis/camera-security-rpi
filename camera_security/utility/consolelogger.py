# consolelogger.py | camera-security-rpi
# Implements the ILogger interface to log messages into console
# Author: Lukas Žaromskis

from camera_security.utility.ilogger import ILogger
from threading import Lock
from datetime import datetime
from camera_security.utility.loglevel import LogLevel


class ConsoleLogger(ILogger):

    __level_text = {LogLevel.NONE: "",
                    LogLevel.INFO: "(INFO) ",
                    LogLevel.ERROR: "(ERROR) ",
                    LogLevel.WARNING: "(WARNING) "}

    def __init__(self):
        self.__lock = Lock()

    def Log(self, message: str, level: LogLevel = LogLevel.INFO):
        self.__lock.acquire()
        print(''.join([str(datetime.utcnow()), ": ", ConsoleLogger.__level_text[level], message]))
        self.__lock.release()

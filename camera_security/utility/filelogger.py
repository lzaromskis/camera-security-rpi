# filelogger.py | camera-security-rpi
# Implements the ILogger interface to log messages into a file
# Author: Lukas Žaromskis

from camera_security.utility.ilogger import ILogger
from threading import Lock
from datetime import datetime
from camera_security.utility.loglevel import LogLevel


class FileLogger(ILogger):
    __level_text = {LogLevel.NONE: "",
                    LogLevel.INFORMATION: "(INFO) ",
                    LogLevel.ERROR: "(ERROR) ",
                    LogLevel.WARNING: "(WARNING) "}

    def __init__(self, file_path: str, append: bool = False):
        self.__lock = Lock()
        self.__append = append
        if append:
            mode = "a"
        else:
            mode = "w"
        self.__file = open(file_path, mode)

    def __del__(self):
        self.__file.close()

    def Log(self, message: str, level: LogLevel = LogLevel.NONE):
        self.__lock.acquire()
        self.__file.write(''.join([str(datetime.utcnow()), ": ", FileLogger.__level_text[level], message]))
        self.__file.flush()
        self.__lock.release()

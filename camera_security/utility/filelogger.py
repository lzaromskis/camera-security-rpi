# filelogger.py | camera-security-rpi
# Implements the ILogger interface to log messages into a file
# Author: Lukas Žaromskis


from camera_security.utility.ilogger import ILogger
from threading import Lock
from datetime import datetime


class FileLogger(ILogger):

    def __init__(self, file_path: str, append: bool = False):
        self.__lock = Lock()
        if append:
            mode = "a"
        else:
            mode = "w"
        self.__file = open(file_path, mode)

    def __del__(self):
        self.__file.close()

    def Log(self, message: str):
        self.__lock.acquire()
        self.__file.write(str(datetime.utcnow()) + ": " + message)
        self.__lock.release()

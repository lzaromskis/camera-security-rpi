# consolelogger.py | camera-security-rpi
# Implements the ILogger interface to log messages into console
# Author: Lukas Žaromskis


from camera_security.utility.ilogger import ILogger
from threading import Lock
from datetime import datetime


class ConsoleLogger(ILogger):

    def __init__(self):
        self.__lock = Lock()

    def Log(self, message: str):
        self.__lock.acquire()
        print(str(datetime.utcnow()) + ": " + message)
        self.__lock.release()

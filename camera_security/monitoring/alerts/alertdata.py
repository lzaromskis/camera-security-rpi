# alertdata.py | camera-security-rpi
# Describes the AlertData class for storing alert data
# Author: Lukas Žaromskis

from camera_security.image.frame import Frame


class AlertData:

    def __init__(self, timestamp: str, image: Frame):
        self.__timestamp = timestamp
        self.__image = image

    def GetTimestamp(self) -> str:
        """
        Returns the alert timestamp
        """
        return self.__timestamp

    def GetImage(self) -> Frame:
        """
        Returns the alert image
        """
        return self.__image

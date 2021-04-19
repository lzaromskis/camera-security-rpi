# detectiondata.py | camera-security-rpi
# Describes the DetectionData class for storing detection data
# Author: Lukas Žaromskis
from camera_security.utility.boundingbox import BoundingBox


class DetectionData:

    def __init__(self, bounding_box: BoundingBox, label: str, certainty: float):
        self.__bounding_box = bounding_box
        self.__label = label
        self.__certainty = certainty

    def GetBoundingBox(self) -> BoundingBox:
        return self.__bounding_box

    def GetLabel(self) -> str:
        return self.__label

    def GetCertainty(self) -> float:
        return self.__certainty

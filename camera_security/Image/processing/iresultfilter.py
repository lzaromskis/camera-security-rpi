# iresultfilter.py | camera-security-rpi
# Describes the IResultFilter interface for filtering the result data list
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import List

from camera_security.Image.processing.detectiondata import DetectionData


class IResultFilter(ABC):

    @abstractmethod
    def Filter(self, data: List[DetectionData]) -> List[DetectionData]:
        """
        Filters the given list
        """
        raise NotImplementedError()

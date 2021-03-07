# iframeprocessor.py | camera-security-rpi
# Describes the IFrameProcessor interface for processing the image to get object detections
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import List
from camera_security.Image.frame import Frame
from camera_security.Image.processing.detectiondata import DetectionData


class IFrameProcessor(ABC):

    @abstractmethod
    def ProcessFrame(self, frame: Frame) -> List[DetectionData]:
        """
        Process
        """
        raise NotImplementedError()

    @abstractmethod
    def GetInputWidth(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def GetInputHeight(self) -> int:
        raise NotImplementedError()

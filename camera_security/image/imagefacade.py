# imagefacade.py | camera-security-rpi
# Describes the ImageFacade class for controlling the image getting and processing subsystem
# Author: Lukas Žaromskis

from typing import List
from camera_security.image.frame import Frame
from camera_security.image.icameraaccessor import ICameraAccessor
from camera_security.image.opencvcameraaccessor import OpenCVCameraAccessor
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iframeprocessor import IFrameProcessor
from camera_security.image.processing.iresultfilter import IResultFilter


class ImageFacade:

    def __init__(self):
        self.__camera_accessor: ICameraAccessor = OpenCVCameraAccessor(0, 640, 480)
        self.__frame_processor: IFrameProcessor = None
        self.__result_filters: List[IResultFilter] = list()

    def RegisterFilter(self, filter: IResultFilter):
        """
        Registers a new result filter.
        Note that expensive filters should be registered last, so they process the fewest elements
        The first filter should be the one which filters out the biggest amount of results
        """
        if not(filter in self.__result_filters):
            self.__result_filters.append(filter)

    def ProcessFrame(self) -> List[DetectionData]:
        """
        Processes a new frame and returns filtered detection results
        """
        frame = self.__camera_accessor.GetNewFrame()
        data = self.__frame_processor.ProcessFrame(frame)

        for filter in self.__result_filters:
            data = filter.Filter(data)

        return data

    def GetFrame(self) -> Frame:
        """
        Returns the previously processed frame
        """
        return self.__camera_accessor.GetFrame()

# imagefacade.py | camera-security-rpi
# Describes the ImageFacade class for controlling the image getting and processing subsystem
# Author: Lukas Žaromskis

from threading import Lock
from typing import List
from camera_security.image.frame import Frame
from camera_security.image.icameraaccessor import ICameraAccessor
from camera_security.image.opencvcameraaccessor import OpenCVCameraAccessor
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iframeprocessor import IFrameProcessor
from camera_security.image.processing.iresultfilter import IResultFilter
from camera_security.image.processing.tensorflowprocessor import TensorflowProcessor
from camera_security.utility.ilogger import ILogger


class ImageFacade:

    def __init__(self, camera_id: int, camera_width: int, camera_height: int, model_filename: str, labels_filename: str, logger: ILogger):
        self.__logger = logger
        self.__camera_accessor: ICameraAccessor = OpenCVCameraAccessor(camera_id, camera_width, camera_height)
        self.__frame_processor: IFrameProcessor = TensorflowProcessor(model_filename, labels_filename, self.__logger)
        self.__result_filters: List[IResultFilter] = list()
        self.__detection_cache: List[DetectionData] = list()
        self.__lock = Lock()

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

        self.__lock.acquire()
        self.__detection_cache = data
        self.__lock.release()
        return data

    def GetPreviousDetections(self) -> List[DetectionData]:
        """
        Returns the previous detection results
        """
        self.__lock.acquire()
        data = self.__detection_cache
        self.__lock.release()
        return data

    def GetFrame(self) -> Frame:
        """
        Returns the previously processed frame
        """
        return self.__camera_accessor.GetFrame()

    def RefreshFrame(self):
        """
        Puts a new frame to the processed frame cache
        (Should be called if processing is skipped)
        """
        self.__camera_accessor.GetNewFrame()

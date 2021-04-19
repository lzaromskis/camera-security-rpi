# heatmapfacade.py | camera-security-rpi
# Describes the HeatmapFacade class for controlling the actions with heatmaps
# Author: Lukas Žaromskis

import cv2
import numpy as np
from typing import List

from camera_security.image.frame import Frame
from camera_security.image.iimagedrawer import IImageDrawer
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.monitoring.heatmap.heatmapdata import HeatmapData
from camera_security.monitoring.heatmap.heatmapstore import HeatmapStore


class HeatmapFacade:

    def __init__(self, time_to_store: float):
        self.__heatmap_data = HeatmapStore(time_to_store)

    def AddData(self, detections: List[DetectionData], delta_time: float):
        bounds_list = list()
        for detection in detections:
            bounds_list.append(detection.GetBoundingBox())
        self.__heatmap_data.AddData(HeatmapData(bounds_list, delta_time))

    def GetHeatmap(self, camera_frame: Frame) -> Frame:
        cam_data = camera_frame.GetData()
        dimensions = cam_data.shape
        height = dimensions[0]
        width = dimensions[1]
        heat = np.zeros((height, width, 1), np.float32)

        time_to_store = self.__heatmap_data.GetTimeToStore()
        heat_data = self.__heatmap_data.GetDataCopy()
        for data in heat_data:
            time = data.GetTime()
            time_normalized = time / time_to_store
            bounds_list = data.GetBoundingBoxes()
            for bounds in bounds_list:
                top_left, bottom_right = bounds.GetCoordinatesInPixels(width, height)
                for y in range(top_left[1], bottom_right[1]):
                    for x in range(top_left[0], bottom_right[0]):
                        heat[y][x] = heat[y][x] + time_normalized

        scaled = (heat_data + 1) * 255 / 2
        color_map = cv2.applyColorMap(scaled, cv2.COLORMAP_JET)
        blended = cv2.addWeighted(camera_frame.GetData(), 0.5, color_map, 0.5, 0.0)
        cv2.imshow("image", blended)
        cv2.waitKey(0)
        return Frame(blended)

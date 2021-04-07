# tensorflowprocessor.py | camera-security-rpi
# Implements the IFrameProcessor interface for detecting objects in images
# Author: Lukas Žaromskis

from typing import List, Any, Dict
import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
from camera_security.image.frame import Frame
from camera_security.utility.boundingbox import BoundingBox
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iframeprocessor import IFrameProcessor
from camera_security.utility.ilogger import ILogger
from camera_security.utility.loglevel import LogLevel


class TensorflowProcessor(IFrameProcessor):

    def __init__(self, model_path: str, label_path: str, logger: ILogger):
        self.__logger = logger
        self.__labels = self.__ReadLabels(label_path)
        self.__interpreter = tflite.Interpreter(model_path)
        self.__interpreter.allocate_tensors()
        _, input_height, input_width, _ = self.__interpreter.get_input_details()[0]['shape']
        self.__input_width = input_width
        self.__input_height = input_height

    def ProcessFrame(self, frame: Frame) -> List[DetectionData]:
        # Set input
        self.__SetInputTensor(frame)
        self.__interpreter.invoke()

        # Get output
        boxes = self.__GetOutputTensor(0)
        classes = self.__GetOutputTensor(1)
        scores = self.__GetOutputTensor(2)
        count = int(self.__GetOutputTensor(3))

        # Process output
        data = list()
        for i in range(count):
            try:
                detection = self.__BuildDetectionData(boxes[i], int(classes[i]), scores[i])
                data.append(detection)
            except IndexError:
                self.__logger.Log(''.join(["Failed to create detection data with data: ", str(boxes[i]), " | ", str(classes[i]), " | ", str(scores[i])]),
                                  LogLevel.WARNING)
        return data

    def GetInputWidth(self) -> int:
        return self.__input_width

    def GetInputHeight(self) -> int:
        return self.__input_height

    def __BuildDetectionData(self, bounding_box_data, label_index: int, certainty: float) -> DetectionData:
        ymin, xmin, ymax, xmax = bounding_box_data
        bounding_box = BoundingBox(xmin, ymin, xmax, ymax)
        label = self.__labels[label_index]
        certainty = certainty
        return DetectionData(bounding_box, label, certainty)

    def __SetInputTensor(self, frame: Frame):
        tensor_index = self.__interpreter.get_input_details()[0]['index']
        input_tensor = self.__interpreter.tensor(tensor_index)()[0]
        proc_frame = cv2.resize(frame.GetData(), (self.__input_width, self.__input_height))
        proc_frame = cv2.cvtColor(proc_frame, cv2.COLOR_BGR2RGB)
        input_tensor[:, :] = proc_frame

    def __GetOutputTensor(self, index: int) -> Any:
        output_details = self.__interpreter.get_output_details()[index]
        tensor = np.squeeze(self.__interpreter.get_tensor(output_details['index']))
        return tensor

    def __ReadLabels(self, path: str) -> Dict[int, str]:
        labels = dict()
        f = open(path)
        lines = f.readlines()
        f.close()
        for line in lines:
            try:
                split_data = line.split('=')
                if len(split_data) != 2:
                    continue
                labels[int(split_data[0])] = split_data[1].strip()
            except ValueError:
                self.__logger.Log(''.join(["Given line '", line, "' in labels file '", path, "' does not have an integer index"]),
                                  LogLevel.WARNING)
        return labels

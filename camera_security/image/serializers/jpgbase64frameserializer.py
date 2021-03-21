# jpgbase64frameserializer.py | camera-security-rpi
# Implements the IFrameSerializer interface with class JpgBase64FrameSerializer for serializing frames into strings
# The class converts the frame to a Jpg image and then encodes it using Base64 encoding
# Author: Lukas Žaromskis

import base64
import cv2
from camera_security.image.frame import Frame
from camera_security.image.serializers.iframeserializer import IFrameSerializer


class JpgBase64FrameSerializer(IFrameSerializer):

    def Serialize(self, data: Frame) -> str:
        is_success, buffer = cv2.imencode(".jpg", data.GetData())
        if is_success:
            b64_data = base64.b64encode(buffer)
            return b64_data.decode('ascii')
        else:
            return ""

    def Deserialize(self, data: str) -> Frame:
        raise NotImplementedError("Currently not implemented. Low priority. Might be removed.")

# getimagerequest.py | camera-security-rpi
# Implements the IRequest interface for getting a frame
# Author: Lukas Žaromskis
import cv2

from camera_security.image.colour import Colour
from camera_security.image.frame import Frame
from camera_security.image.iimagedrawer import IImageDrawer
from camera_security.image.serializers.iframeserializer import IFrameSerializer
from camera_security.image.imagefacade import ImageFacade
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.utility.boundingbox import BoundingBox


class GetImageRequest(RequestWithAuthentication):

    def __init__(self, image_facade: ImageFacade, monitoring_facade: MonitoringFacade, image_drawer: IImageDrawer, frame_serializer: IFrameSerializer):
        self.__image_facade = image_facade
        self.__monitoring_facade = monitoring_facade
        self.__image_drawer = image_drawer
        self.__frame_serializer = frame_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        frame = self.__image_facade.GetFrame()
        new_frame = Frame(frame.GetData().copy())
        draw_zones = data.GetAttribute(PacketAttribute.DRAW_ZONES)
        draw_detections = data.GetAttribute(PacketAttribute.DRAW_DETECTIONS)
        if draw_zones is not None and draw_zones == "true":
            zones = self.__monitoring_facade.GetZones()
            for zone in zones:
                if zone.IsActive():
                    colour = Colour.GREEN
                else:
                    colour = Colour.RED
                self.__image_drawer.DrawRectangle(new_frame, zone.GetBounds(), colour, 3)

        if draw_detections is not None and draw_detections == "true":
            detections = self.__image_facade.GetPreviousDetections()
            for detection in detections:
                bounds = detection.GetBoundingBox()
                self.__image_drawer.DrawRectangle(new_frame, bounds, Colour.YELLOW, 3)
                self.__image_drawer.DrawText(new_frame, detection.GetLabel().upper(), bounds.GetCoordinates()[0], cv2.FONT_HERSHEY_COMPLEX,
                                             1, 1, Colour.BLACK, Colour.YELLOW)

        serialized_frame = self.__frame_serializer.Serialize(new_frame)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending image JPG encoded in BASE64")
        packet.AddAttribute(PacketAttribute.IMAGE, serialized_frame)
        return packet

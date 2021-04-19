# getimagerequest.py | camera-security-rpi
# Implements the IRequest interface for getting a frame
# Author: Lukas Žaromskis

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
from camera_security.monitoring.heatmap.heatmapfacade import HeatmapFacade
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.utility.boundingbox import BoundingBox


class GetHeatmapRequest(RequestWithAuthentication):

    def __init__(self, image_facade: ImageFacade, heatmap_facade: HeatmapFacade, frame_serializer: IFrameSerializer):
        self.__image_facade = image_facade
        self.__heatmap_facade = heatmap_facade
        self.__frame_serializer = frame_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        frame = self.__image_facade.GetFrame()
        new_frame = Frame(frame.GetData().copy())

        heatmap = self.__heatmap_facade.GetHeatmap(new_frame)

        serialized_frame = self.__frame_serializer.Serialize(heatmap)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending heatmap image JPG encoded in BASE64")
        packet.AddAttribute(PacketAttribute.IMAGE, serialized_frame)
        return packet

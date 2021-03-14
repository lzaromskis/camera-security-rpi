# getimagerequest.py | camera-security-rpi
# Implements the IRequest interface for getting a frame
# Author: Lukas Žaromskis

from camera_security.image.helpers.iframeserializer import IFrameSerializer
from camera_security.image.imagefacade import ImageFacade
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode


class GetImageRequest(RequestWithAuthentication):

    def __init__(self, image_facade: ImageFacade, frame_serializer: IFrameSerializer):
        self.__image_facade = image_facade
        self.__frame_serializer = frame_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        frame = self.__image_facade.GetFrame()
        serialized_frame = self.__frame_serializer.Serialize(frame)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending image JPG encoded in BASE64")
        packet.AddAttribute(PacketAttribute.IMAGE, serialized_frame)
        return packet

# getdataforcreatingzonerequest.py | camera-security-rpi
# Implements the IRequest interface for getting a frame
# Author: Lukas Žaromskis
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.image.imagefacade import ImageFacade
from camera_security.image.serializers.iframeserializer import IFrameSerializer


class GetDataForCreatingZoneRequest(RequestWithAuthentication):

<<<<<<< HEAD
    def __init__(self, labels: str, image_facade: ImageFacade, frame_serializer: IFrameSerializer):
        self.__labels = labels
        self.__image_facade = image_facade
        self.__serializer = frame_serializer

=======
>>>>>>> main
    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        frame = self.__image_facade.GetFrame()
        serialized_frame = self.__serializer.Serialize(frame)

        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending heatmap image JPG encoded in BASE64")
        packet.AddAttribute(PacketAttribute.IMAGE, serialized_frame)
        packet.AddAttribute(PacketAttribute.LABELS, self.__labels)
<<<<<<< HEAD
        return packet
=======
        return packet

    def __init__(self, labels: str, image_facade: ImageFacade, frame_serializer: IFrameSerializer):
        self.__labels = labels
        self.__image_facade = image_facade
        self.__serializer = frame_serializer
>>>>>>> main

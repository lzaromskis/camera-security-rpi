# getlatestalertsrequest.py | camera-security-rpi
# Implements the IRequest interface for getting an image of an alert
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.image.serializers.iframeserializer import IFrameSerializer
from camera_security.monitoring.alerts.alertsfacade import AlertsFacade
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class GetAlertImageRequest(RequestWithAuthentication):

    def __init__(self, alerts_facade: AlertsFacade, frame_serializer: IFrameSerializer):
        self.__alerts_facade = alerts_facade
        self.__frame_serializer = frame_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        timestamp = data.GetAttribute(PacketAttribute.ALERT)
        if timestamp is None:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ALERT)

        try:
            image = self.__alerts_facade.GetAlert(timestamp)
        except FileNotFoundError:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ALERT)

        serialized_frame = self.__frame_serializer.Serialize(image)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending alert image")
        packet.AddAttribute(PacketAttribute.IMAGE, serialized_frame)
        return packet

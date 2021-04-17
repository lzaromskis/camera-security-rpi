# getlatestalertsrequest.py | camera-security-rpi
# Implements the IRequest interface for getting a list of latest alerts
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.alerts.alertsfacade import AlertsFacade
from camera_security.utility.serializers.istringlistserializer import IStringListSerializer


class GetLatestAlertsRequest(RequestWithAuthentication):

    def __init__(self, alerts_facade: AlertsFacade, list_serializer: IStringListSerializer):
        self.__alerts_facade = alerts_facade
        self.__list_serializer = list_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        alerts = self.__alerts_facade.GetAvailableAlerts()
        alerts.sort(reverse=True)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending latest alerts")
        packet.AddAttribute(PacketAttribute.ALERT_LIST, self.__list_serializer.Serialize(alerts))
        return packet

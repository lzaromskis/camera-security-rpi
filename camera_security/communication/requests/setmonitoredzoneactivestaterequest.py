# setmonitoredzoneactivestaterequest.py | camera-security-rpi
# Implements the IRequest interface for getting a frame
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.monitoringfacade import MonitoringFacade


class SetMonitoredZoneActiveStateRequest(RequestWithAuthentication):

    def __init__(self, monitoring_facade: MonitoringFacade):
        self.__monitoring_facade = monitoring_facade

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        zone_name = data.GetAttribute(PacketAttribute.ZONE_NAME)
        if zone_name is None:
            default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ZONE_NAME)
        zone_state = data.AddAttribute(PacketAttribute.ZONE_ACTIVE)
        if zone_state is None:
            default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ZONE_ACTIVE)

        packet = PacketData()

        zone = self.__monitoring_facade.GetZone(zone_name)
        if zone is None:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_DATA.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Could not find zone with the given name")
            return packet

        zone.SetActive(zone_state == "true")
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone active state set successfully")
        return packet

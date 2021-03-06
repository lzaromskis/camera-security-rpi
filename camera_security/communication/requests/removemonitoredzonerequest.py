# removemonitoredzonerequest.py | camera-security-rpi
# Implements the IRequest interface for removing a monitored zone
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.monitoringfacade import MonitoringFacade


class RemoveMonitoredZoneRequest(RequestWithAuthentication):

    def __init__(self, monitoring_facade: MonitoringFacade):
        self.__monitoring_facade = monitoring_facade

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        zone_name = data.GetAttribute(PacketAttribute.ZONE_NAME)
        if zone_name is None:
            default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ZONE_NAME)

        ret_val = self.__monitoring_facade.RemoveZone(zone_name)
        packet = PacketData()
        if ret_val:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone removed successfully")
        else:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_DATA.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Failed to remove monitored zone: does not exist")
        return packet

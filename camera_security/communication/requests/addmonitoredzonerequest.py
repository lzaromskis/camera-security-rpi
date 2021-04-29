# addmonitoredzonerequest.py | camera-security-rpi
# Implements the IRequest interface for adding a monitored zone
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.monitoring.serializers.imonitoredzoneserializer import IMonitoredZoneSerializer
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError


class AddMonitoredZoneRequest(RequestWithAuthentication):

    def __init__(self, monitoring_facade: MonitoringFacade, zone_serializer: IMonitoredZoneSerializer):
        self.__monitoring_facade = monitoring_facade
        self.__zone_serializer = zone_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        zone_data = data.GetAttribute(PacketAttribute.ZONE)
        if zone_data is None:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ZONE)

        try:
            zone = self.__zone_serializer.Deserialize(zone_data)
        except DeserializationFailedError:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.ZONE)

        packet = PacketData()

        top_left, bottom_right = zone.GetBounds().GetCoordinates()
        if top_left[0] >= bottom_right[0] or top_left[1] >= bottom_right[1]:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_DATA.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone bounds have bad coordinates")

        if len(zone.GetLabels()) == 0:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_DATA.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone has no labels")

        ret_val = self.__monitoring_facade.AddZone(zone)

        if ret_val:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone added successfully")
        else:
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_DATA.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Monitored zone with the given name already exists")
        return packet

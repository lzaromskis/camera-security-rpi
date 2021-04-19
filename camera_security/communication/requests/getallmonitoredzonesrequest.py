# getallmonitoredzonesrequest.py | camera-security-rpi
# Implements the IRequest interface for getting all monitored zones
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.monitoring.monitoringfacade import MonitoringFacade
from camera_security.monitoring.serializers.imonitoredzonecollectionserializer import IMonitoredZoneCollectionSerializer


class GetAllMonitoredZonesRequest(RequestWithAuthentication):

    def __init__(self, monitoring_facade: MonitoringFacade, zones_serializer: IMonitoredZoneCollectionSerializer):
        self.__monitoring_facade = monitoring_facade
        self.__zones_serializer = zones_serializer

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        zones = self.__monitoring_facade.GetCollection()
        serialized_zones = self.__zones_serializer.Serialize(zones)
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "Sending monitored zones data")
        packet.AddAttribute(PacketAttribute.ZONES, serialized_zones)
        return packet

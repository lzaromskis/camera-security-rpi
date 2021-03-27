# monitoring.py | camera-security-rpi
# Describes the MonitoringFacade class for controlling the monitoring zones facade
# Author: Lukas Žaromskis
from typing import List

from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.monitoring.monitoredzonecollectionio import MonitoredZoneCollectionIO
from camera_security.monitoring.serializers.monitoredzonecollectionserializer import MonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
from camera_security.utility.boundingbox import BoundingBox
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer


class MonitoringFacade:

    def __init__(self, monitored_zones_filename: str):
        self.__monitored_zones_filename = monitored_zones_filename
        self.__monitored_zones_io = MonitoredZoneCollectionIO(MonitoredZoneCollectionSerializer(MonitoredZoneSerializer(BoundingBoxSerializer())))
        try:
            self.__monitored_zones = self.__monitored_zones_io.GetMonitoredZones(self.__monitored_zones_filename)
        except FileNotFoundError:
            self.__monitored_zones = MonitoredZoneCollection()

    def SetZoneActiveState(self, zone_name: str, active: bool):
        zone = self.__monitored_zones.GetZone(zone_name)
        if zone:
            zone.SetActive(active)

    def AddZone(self, zone: MonitoredZone) -> bool:
        if self.__monitored_zones.AddZone(zone):
            self.__monitored_zones_io.SaveMonitoredZones(self.__monitored_zones)
            return True
        return False

    def RemoveZone(self, zone_name: str):
        if self.__monitored_zones.RemoveZone(zone_name):
            self.__monitored_zones_io.SaveMonitoredZones()

    def GetCollisions(self, detected: List[BoundingBox]) -> List[MonitoredZone]:
        ret_list = list()
        for zone in self.__monitored_zones.GetAllZones():
            if zone.IsActive():
                bounds = zone.GetBounds()
                for d in detected:
                    if bounds.IsColliding(d):
                        ret_list.append(zone)
                        break
        return ret_list

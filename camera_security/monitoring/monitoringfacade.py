# monitoring.py | camera-security-rpi
# Describes the MonitoringFacade class for controlling the monitoring zones facade
# Author: Lukas Žaromskis
from typing import List, Optional

from camera_security.image.processing.detectiondata import DetectionData
from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.monitoring.monitoredzonecollectionio import MonitoredZoneCollectionIO
from camera_security.monitoring.serializers.monitoredzonecollectionserializer import MonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
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
            self.__monitored_zones_io.SaveMonitoredZones(self.__monitored_zones, self.__monitored_zones_filename)
            return True
        return False

    def GetZone(self, zone_name: str) -> Optional[MonitoredZone]:
        return self.__monitored_zones.GetZone(zone_name)

    def RemoveZone(self, zone_name: str) -> bool:
        ret_val = self.__monitored_zones.RemoveZone(zone_name)
        if ret_val:
            self.__monitored_zones_io.SaveMonitoredZones(self.__monitored_zones_filename)
        return ret_val

    def GetCollidingZones(self, detected: List[DetectionData]) -> List[MonitoredZone]:
        ret_list = list()
        for zone in self.__monitored_zones.GetAllZones():
            if zone.IsActive():
                bounds = zone.GetBounds()
                for d in detected:
                    if bounds.IsColliding(d.GetBoundingBox()):
                        ret_list.append(zone)
                        break
        return ret_list

    def GetZones(self) -> List[MonitoredZone]:
        return self.__monitored_zones.GetAllZones()

    def GetCollection(self) -> MonitoredZoneCollection:
        return self.__monitored_zones

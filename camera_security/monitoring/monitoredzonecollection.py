# monitoredzonecollection.py | camera-security-rpi
# Describes the MonitoredZoneCollection for storing multiple monitored zones
# Author: Lukas Žaromskis

from typing import Optional, List
from camera_security.monitoring.monitoredzone import MonitoredZone


class MonitoredZoneCollection:

    def __init__(self):
        self.__zones = dict()

    def AddZone(self, zone: MonitoredZone) -> bool:
        """
        Add the given zone to the collections. Returns false if the zone already exists with the given name.
        """
        name = zone.GetName()
        if name in self.__zones:
            return False
        self.__zones[name] = zone
        return True

    def GetZone(self, name: str) -> Optional[MonitoredZone]:
        """
        Returns a MonitoredZone with the given name. Returns None if the zone does not exist in collection.
        """
        try:
            zone = self.__zones[name]
            return zone
        except KeyError:
            return None

    def GetAllZones(self) -> List[MonitoredZone]:
        """
        Returns all zones in the collection
        """
        return list(self.__zones.values())

    def RemoveZone(self, name: str) -> bool:
        """
        Deletes a monitored zone with the given name from the collection. Returns true if the deletion was successful
        """
        try:
            del self.__zones[name]
            return True
        except KeyError:
            return False

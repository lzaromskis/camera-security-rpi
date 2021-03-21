# monitoredzonecollectionserializer.py | camera-security-rpi
# Implements the MonitoredZoneCollectionSerializer interface for serializing monitored zone collections
# Author: Lukas Žaromskis
from io import StringIO

from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.monitoring.serializers.imonitoredzonecollectionserializer import IMonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.imonitoredzoneserializer import IMonitoredZoneSerializer
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError


class MonitoredZoneCollectionSerializer(IMonitoredZoneCollectionSerializer):

    ZONE_SEPARATOR = '?'

    def __init__(self, zone_serializer: IMonitoredZoneSerializer):
        self.__zone_serializer = zone_serializer

    def Serialize(self, data: MonitoredZoneCollection) -> str:
        if type(data) != MonitoredZoneCollection:
            raise TypeError("Data is not a MonitoredZoneCollection")
        string_io = StringIO()
        for zone in data.GetAllZones():
            string_io.write()
        string_data = string_io.getvalue()
        string_io.close()
        return string_data

    def Deserialize(self, data: str) -> MonitoredZoneCollection:
        try:
            split_data = data.split(self.ZONE_SEPARATOR)
            collection = MonitoredZoneCollection()
            for z in split_data:
                zone = self.__zone_serializer.Deserialize(z)
                collection.AddZone(zone)
            return collection
        except Exception:
            raise DeserializationFailedError("Failed to deserialize string to a MonitoredZoneCollection")

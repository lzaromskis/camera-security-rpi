# monitoredzoneserializer.py | camera-security-rpi
# Implements the IMonitoredZoneSerializer interface for serializing monitored zones
# Author: Lukas Žaromskis

from io import StringIO
from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.serializers.imonitoredzoneserializer import IMonitoredZoneSerializer
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError
from camera_security.utility.serializers.iboundingboxserializer import IBoundingBoxSerializer


class MonitoredZoneSerializer(IMonitoredZoneSerializer):

    DATA_SEPARATOR = '!'

    def __init__(self, bounds_serializer: IBoundingBoxSerializer):
        self.__bounds_serializer = bounds_serializer

    def Serialize(self, data: MonitoredZone) -> str:
        if type(data) != MonitoredZone:
            raise TypeError("Data is not a MonitoredZone")
        string_io = StringIO()
        string_io.write(''.join([data.GetName(),
                                 self.DATA_SEPARATOR,
                                 self.__bounds_serializer.Serialize(data.GetBounds()),
                                 self.DATA_SEPARATOR,
                                 str(data.IsActive())]))
        string_data = string_io.getvalue()
        string_io.close()
        return string_data

    def Deserialize(self, data: str) -> MonitoredZone:
        try:
            split_data = data.split(self.DATA_SEPARATOR)
            zone = MonitoredZone(split_data[0],
                                 self.__bounds_serializer.Deserialize(split_data[1]))
            zone.SetActive(split_data[2] == "true")
            return zone
        except Exception:
            raise DeserializationFailedError("Failed to deserialize string to a MonitoredZone")

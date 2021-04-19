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
    LABELS_SEPARATOR = ','

    def __init__(self, bounds_serializer: IBoundingBoxSerializer):
        self.__bounds_serializer = bounds_serializer

    def Serialize(self, data: MonitoredZone) -> str:
        if type(data) != MonitoredZone:
            raise TypeError("Data is not a MonitoredZone")
        name = data.GetName()
        bounds = self.__bounds_serializer.Serialize(data.GetBounds())
        active = str(data.IsActive())
        labels = self.LABELS_SEPARATOR.join(data.GetLabels())
        return self.DATA_SEPARATOR.join([name, bounds, active, labels])

    def Deserialize(self, data: str) -> MonitoredZone:
        try:
            split_data = data.split(self.DATA_SEPARATOR)
            labels = list()
            split_labels = split_data[3].split(self.LABELS_SEPARATOR)
            for lab in split_labels:
                stripped = lab.strip()
                if stripped != "":
                    labels.append(lab)
            zone = MonitoredZone(split_data[0],
                                 self.__bounds_serializer.Deserialize(split_data[1]), labels)
            zone.SetActive(split_data[2] == "True")
            return zone
        except Exception:
            raise DeserializationFailedError("Failed to deserialize string to a MonitoredZone")

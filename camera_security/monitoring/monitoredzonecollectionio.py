# monitoredzonecollectionio.py | camera-security-rpi
# Implements the MonitoredZoneCollectionIO interface for reading and writing monitored zone collection data
# Author: Lukas Žaromskis

from os import path
from camera_security.monitoring.imonitoredzonecollectionio import IMonitoredZoneCollectionIO
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.monitoring.serializers.imonitoredzonecollectionserializer import IMonitoredZoneCollectionSerializer
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError
from camera_security.utility.exceptions.invalidfileerror import InvalidFileError


class MonitoredZoneCollectionIO(IMonitoredZoneCollectionIO):

    MAGIC = "CSmz"

    def __init__(self, collection_serializer: IMonitoredZoneCollectionSerializer):
        self.__collection_serializer = collection_serializer

    def GetMonitoredZones(self, filename: str) -> MonitoredZoneCollection:
        if not path.isfile(filename):
            raise FileNotFoundError("File \"" + filename + "\" does not exist!")
        f = open(filename, "r")
        raw_data = f.readline()
        if not raw_data.startswith(self.MAGIC):
            f.close()
            raise InvalidFileError("File \"" + filename + "\" is not a valid monitored zone collection file!")
        split_data = raw_data.split("|")
        if len(split_data) != 2:
            f.close()
            raise InvalidFileError(
                "File \"" + filename + "\" must contain only 3 data attributes: magic number, hash and salt!")
        ret_val = self.__collection_serializer.Deserialize(split_data[1])
        f.close()
        return ret_val

    def SaveMonitoredZones(self, zones: MonitoredZoneCollection, filename: str):
        f = open(filename, "w")
        f.write(''.join([self.MAGIC, "|", self.__collection_serializer.Serialize(zones)]))
        f.close()

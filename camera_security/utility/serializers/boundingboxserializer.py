# boundingboxserializer.py | camera-security-rpi
# Implements the IBoundingBoxSerializer interface for serializing bounding boxes
# Author: Lukas Žaromskis

from io import StringIO
from camera_security.utility.boundingbox import BoundingBox
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError
from camera_security.utility.serializers.iboundingboxserializer import IBoundingBoxSerializer


class BoundingBoxSerializer(IBoundingBoxSerializer):

    COORDINATE_SEPARATOR = ','

    def Serialize(self, data: BoundingBox) -> str:
        if type(data) != BoundingBox:
            raise TypeError("Data must be a BoundingBox")
        top_left, bottom_right = data.GetCoordinates()
        return self.COORDINATE_SEPARATOR.join([str(top_left[0]), str(top_left[1]), str(bottom_right[0]), str(bottom_right[1])])

    def Deserialize(self, data: str) -> BoundingBox:
        if type(data) != str:
            raise TypeError("Data must be a string")
        try:
            split_data = data.split(self.COORDINATE_SEPARATOR)
            bounds = BoundingBox(float(split_data[0]),
                                 float(split_data[1]),
                                 float(split_data[2]),
                                 float(split_data[3]))
            return bounds
        except Exception:
            raise DeserializationFailedError("Failed to deserialize the given string to a bounding box")

import unittest

from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
from camera_security.utility.boundingbox import BoundingBox
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer


class MonitoredZoneSerializerTests(unittest.TestCase):
    def test_serialize(self):
        # Arrange
        name = "test_zone"
        bounds = BoundingBox(1, 1, 5, 5)
        labels = ["label1", "label2"]
        zone = MonitoredZone(name, bounds, labels)
        expected = "test_zone!1,1,5,5!False!label1,label2"
        serializer = MonitoredZoneSerializer(BoundingBoxSerializer())

        # Act
        result = serializer.Serialize(zone)

        # Assert
        self.assertEqual(result, expected)

    def test_deserialize_success(self):
        # Arrange
        name = "test_zone"
        bounds = BoundingBox(1, 1, 5, 5)
        labels = ["label1", "label2"]
        data = "test_zone!1,1,5,5!False!label1,label2"
        serializer = MonitoredZoneSerializer(BoundingBoxSerializer())

        # Act
        result = serializer.Deserialize(data)

        # Assert
        self.assertEqual(result.GetName(), name)
        self.assertEqual(result.GetBounds(), bounds)
        self.assertFalse(result.IsActive())
        self.assertEqual(result.GetLabels(), labels)

    def test_deserialize_raises_error(self):
        # Arrange
        data = "test_zone!1,1,5,5!False"
        serializer = MonitoredZoneSerializer(BoundingBoxSerializer())

        # Act
        # Assert
        with self.assertRaises(DeserializationFailedError) as error:
            serializer.Deserialize(data)
        self.assertEqual("Failed to deserialize string to a MonitoredZone", error.exception.message)


if __name__ == '__main__':
    unittest.main()

import unittest

from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.monitoring.serializers.monitoredzonecollectionserializer import MonitoredZoneCollectionSerializer
from camera_security.monitoring.serializers.monitoredzoneserializer import MonitoredZoneSerializer
from camera_security.utility.boundingbox import BoundingBox
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer


class MonitoredZoneCollectionSerializerTests(unittest.TestCase):
    def test_serialize(self):
        # Arrange
        name1 = "test_zone1"
        bounds1 = BoundingBox(1, 1, 5, 5)
        labels1 = ["label1", "label2"]
        zone1 = MonitoredZone(name1, bounds1, labels1)
        name2 = "test_zone2"
        bounds2 = BoundingBox(2, 2, 5, 5)
        labels2 = ["label1", "label2"]
        zone2 = MonitoredZone(name2, bounds2, labels2)
        collection = MonitoredZoneCollection()
        collection.AddZone(zone1)
        collection.AddZone(zone2)
        expected = "test_zone1!1,1,5,5!False!label1,label2?test_zone2!2,2,5,5!False!label1,label2"
        serializer = MonitoredZoneCollectionSerializer(MonitoredZoneSerializer(BoundingBoxSerializer()))

        # Act
        result = serializer.Serialize(collection)

        # Assert
        self.assertEqual(result, expected)

    def test_deserialize_success(self):
        # Arrange
        name1 = "test_zone1"
        bounds1 = BoundingBox(1, 1, 5, 5)
        labels1 = ["label1", "label2"]
        zone1 = MonitoredZone(name1, bounds1, labels1)
        name2 = "test_zone2"
        bounds2 = BoundingBox(2, 2, 5, 5)
        labels2 = ["label1", "label2"]
        zone2 = MonitoredZone(name2, bounds2, labels2)
        collection = MonitoredZoneCollection()
        collection.AddZone(zone1)
        collection.AddZone(zone2)
        data = "test_zone1!1,1,5,5!False!label1,label2?test_zone2!2,2,5,5!False!label1,label2"
        serializer = MonitoredZoneCollectionSerializer(MonitoredZoneSerializer(BoundingBoxSerializer()))

        # Act
        result = serializer.Deserialize(data)

        # Assert
        zonelist = result.GetAllZones()
        self.assertEqual(zonelist[0].GetName(), name1)
        self.assertEqual(zonelist[0].GetBounds(), bounds1)
        self.assertFalse(zonelist[0].IsActive())
        self.assertEqual(zonelist[0].GetLabels(), labels1)
        self.assertEqual(zonelist[1].GetName(), name2)
        self.assertEqual(zonelist[1].GetBounds(), bounds2)
        self.assertFalse(zonelist[1].IsActive())
        self.assertEqual(zonelist[1].GetLabels(), labels2)


if __name__ == '__main__':
    unittest.main()

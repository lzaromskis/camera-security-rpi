import unittest

from camera_security.monitoring.monitoredzone import MonitoredZone
from camera_security.monitoring.monitoredzonecollection import MonitoredZoneCollection
from camera_security.utility.boundingbox import BoundingBox


class MonitoredZoneCollectionTests(unittest.TestCase):
    def test_AddZone_Once(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"
        bounds = BoundingBox(0, 0, 10, 10)
<<<<<<< HEAD
        labels = ["test_label"]
        zone = MonitoredZone(name, bounds, labels)
=======
        zone = MonitoredZone(name, bounds)
>>>>>>> main

        # Act
        result = collection.AddZone(zone)

        # Assert
        self.assertTrue(result)
        self.assertEqual(zone, collection._MonitoredZoneCollection__zones[name])

    def test_AddZone_Twice(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"
        bounds = BoundingBox(0, 0, 10, 10)
<<<<<<< HEAD
        labels = ["test_label"]
        zone = MonitoredZone(name, bounds, labels)
=======
        zone = MonitoredZone(name, bounds)
>>>>>>> main

        # Act
        result1 = collection.AddZone(zone)
        result2 = collection.AddZone(zone)

        # Assert
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertEqual(zone, collection._MonitoredZoneCollection__zones[name])

    def test_GetZone_Existing(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"
        bounds = BoundingBox(0, 0, 10, 10)
<<<<<<< HEAD
        labels = ["test_label"]
        zone = MonitoredZone(name, bounds, labels)
=======
        zone = MonitoredZone(name, bounds)
>>>>>>> main
        collection._MonitoredZoneCollection__zones[name] = zone

        # Act
        result = collection.GetZone(name)

        # Assert
        self.assertEqual(zone, result)

    def test_GetZone_NonExisting(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"

        # Act
        result = collection.GetZone(name)

        # Assert
        self.assertEqual(None, result)

    def test_GetAllZones_Empty(self):
        # Arrange
        collection = MonitoredZoneCollection()

        # Act
        result = collection.GetAllZones()

        # Assert
        self.assertEqual(0, len(result))

    def test_GetAllZones_MultipleZones(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name1 = "test_zone1"
        name2 = "test_zone2"
        bounds1 = BoundingBox(0, 0, 10, 10)
        bounds2 = BoundingBox(0, 0, 20, 20)
<<<<<<< HEAD
        labels1 = ["test_label1"]
        labels2 = ["test_label2"]
        zone1 = MonitoredZone(name1, bounds1, labels1)
        zone2 = MonitoredZone(name2, bounds2, labels2)
=======
        zone1 = MonitoredZone(name1, bounds1)
        zone2 = MonitoredZone(name2, bounds2)
>>>>>>> main
        collection._MonitoredZoneCollection__zones[name1] = zone1
        collection._MonitoredZoneCollection__zones[name2] = zone2

        # Act
        result = collection.GetAllZones()

        # Assert
        self.assertEqual(2, len(result))
        self.assertTrue(zone1 in result)
        self.assertTrue(zone2 in result)

    def test_DeleteZone_Existing(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"
        bounds = BoundingBox(0, 0, 10, 10)
<<<<<<< HEAD
        labels = ["test_label"]
        zone = MonitoredZone(name, bounds, labels)
=======
        zone = MonitoredZone(name, bounds)
>>>>>>> main
        collection._MonitoredZoneCollection__zones[name] = zone

        # Act
        result = collection.RemoveZone(name)

        # Assert
        self.assertTrue(result)
        with self.assertRaises(KeyError) as error:
            collection._MonitoredZoneCollection__zones[name]

    def test_DeleteZone_NonExisting(self):
        # Arrange
        collection = MonitoredZoneCollection()
        name = "test_zone"

        # Act
        result = collection.RemoveZone(name)

        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

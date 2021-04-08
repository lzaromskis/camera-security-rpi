from datetime import datetime

import numpy as np
import unittest
from os import path
from camera_security.image.frame import Frame
from camera_security.monitoring.alerts.alertdata import AlertData
from camera_security.monitoring.alerts.alertio import AlertIO
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class MyTestCase(unittest.TestCase):
    def test_SaveAlert(self):
        # Arrange
        folder = "./testalerts/"
        filename = "testfile"
        full_path = folder + filename
        io = AlertIO(alerts_folder=folder)
        np_data = np.ndarray((3,), buffer=np.array([1, 2, 3]), dtype=int)
        data = AlertData(filename, Frame(np_data))

        # Act
        io.SaveAlert(data)

        # Assert
        self.assertTrue(path.isfile(full_path))
        with open(full_path, 'rb') as f:
            saved_data = np.load(f)
        self.assertTrue(np.array_equal(np_data, saved_data))

    def test_SaveAlertCulling(self):
        # Arrange
        folder = "./testalerts3/"
        filename = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S_%f")
        full_path = folder + filename
        io = AlertIO(alerts_folder=folder, alerts_to_keep=5)
        np_data = np.ndarray((3,), buffer=np.array([1, 2, 3]), dtype=int)
        data = AlertData(filename, Frame(np_data))

        # Act
        io.SaveAlert(data)
        files = io.GetAvailableAlerts()

        # Assert
        self.assertTrue(path.isfile(full_path))
        self.assertEqual(5, len(files))

    def test_GetAlert(self):
        # Arrange
        folder = "./testalerts/"
        filename = "readfile"
        io = AlertIO(alerts_folder=folder)
        expected_data = np.ndarray((3,), buffer=np.array([1, 2, 3]), dtype=int)

        # Act
        data = io.GetAlert(filename)

        # Assert
        self.assertEqual(filename, data.GetTimestamp())
        self.assertTrue(np.array_equal(expected_data, data.GetImage().GetData()))

    def test_GetAlertNonExisting(self):
        # Arrange
        folder = "./testalerts/"
        filename = "nonexistingfile"
        full_path = folder + filename
        io = AlertIO(alerts_folder=folder)

        # Act
        # Assert
        with self.assertRaises(FileNotFoundError) as error:
            io.GetAlert(filename)
        self.assertEqual("File \"" + full_path + "\" does not exist!", error.exception.message)

    def test_GetAvailableAlerts(self):
        # Arrange
        folder = "./testalerts2/"
        io = AlertIO(alerts_folder=folder)

        # Act
        files = io.GetAvailableAlerts()

        # Assert
        self.assertEqual(4, len(files))
        self.assertTrue("file1" in files)
        self.assertTrue("file2" in files)
        self.assertTrue("file3" in files)
        self.assertTrue("file4" in files)


if __name__ == '__main__':
    unittest.main()

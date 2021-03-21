import unittest
from camera_security.authentication.passwordio import PasswordIO, MAGIC
from camera_security.authentication.passworddata import PasswordData
from camera_security.utility.exceptions.invalidfileerror import InvalidFileError
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class PasswordIOTests(unittest.TestCase):
    def test_GetPassword_FileNotFound(self):
        # Arrange
        io = PasswordIO("some_file")

        # Act and Assert
        with self.assertRaises(FileNotFoundError) as error:
            io.GetPassword()
        self.assertEqual("File \"some_file\" does not exist!", error.exception.message)

    def test_GetPassword_InvalidMagic(self):
        # Arrange
        file_name = "password_invalid_magic"
        io = PasswordIO(file_name)

        # Act and Assert
        with self.assertRaises(InvalidFileError) as error:
            io.GetPassword()
        self.assertEqual("File \"" + file_name + "\" is not a valid password file!", error.exception.message)

    def test_GetPassword_InvalidSplit(self):
        # Arrange
        file_name = "password_invalid_split"
        io = PasswordIO(file_name)

        # Act and Assert
        with self.assertRaises(InvalidFileError) as error:
            io.GetPassword()
        self.assertEqual("File \"" + file_name + "\" must contain only 3 data attributes: magic number, hash and salt!", error.exception.message)

    def test_GetPassword(self):
        # Arrange
        expected_result = PasswordData("hash", "salt")
        file_name = "password_valid"
        io = PasswordIO(file_name)

        # Act
        actual_result = io.GetPassword()

        # Assert
        self.assertEqual(expected_result.GetSalt(), actual_result.GetSalt())
        self.assertEqual(expected_result.GetHash(), actual_result.GetHash())

    def test_SavePassword(self):
        # Arrange
        expected_result = MAGIC + "|hash|salt"
        file_name = "password_valid"
        hash_data = "hash"
        salt_data = "salt"
        io = PasswordIO(file_name)
        data = PasswordData(hash_data, salt_data)

        # Act
        io.SavePassword(data)

        # Assert
        f = open(file_name)
        actual_result = f.readline()
        f.close()
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()

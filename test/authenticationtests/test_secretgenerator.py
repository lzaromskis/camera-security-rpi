import unittest
import string
from camera_security.authentication.isecretgenerator import SecretGenerator


SYMBOLS = string.ascii_letters + string.digits


class SecretGeneratorTests(unittest.TestCase):

    def test_generate(self):
        # Arrange
        generator = SecretGenerator()
        length = 64

        # Act
        result = generator.Generate(length)

        # Assert
        self.assertEqual(length, len(result))
        for c in result:
            self.assertTrue(c in SYMBOLS)


if __name__ == '__main__':
    unittest.main()

# hashsha512.py | camera-security-rpi
# Implements the IHash interface with HashSHA512 class
# Author: Lukas Žaromskis

import hashlib
from camera_security.authentication.ihash import IHash


class HashSHA512(IHash):

    def Hash(self, password: str, salt: str) -> str:
        h = hashlib.sha512()
        h.update((password + salt).encode())
        return h.hexdigest()

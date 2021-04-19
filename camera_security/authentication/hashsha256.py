# hashsha256.py | camera-security-rpi
# Implements the IHash interface with HashSHA256 class
# Author: Lukas Žaromskis

import hashlib
from camera_security.authentication.ihash import IHash


class HashSHA256(IHash):

    def Hash(self, password: str, salt: str) -> str:
        h = hashlib.sha256()
        h.update((password + salt).encode())
        return h.hexdigest()

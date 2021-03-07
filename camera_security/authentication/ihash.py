# ihash.py | camera-security-rpi
# Describes the IHash interface for hashing passwords
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IHash(ABC):

    @abstractmethod
    def Hash(self, password: str, salt: str) -> str:
        """
        Hashes the password and the salt.
        """
        raise NotImplementedError()

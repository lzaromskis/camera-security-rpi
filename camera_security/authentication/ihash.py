# ihash.py | camera-security-rpi
# Describes the IHash interface for hashing passwords
# Implements the interface with HashSHA256 class
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
import hashlib


class IHash(ABC):

    @abstractmethod
    def Hash(self, password: str, salt: str) -> str:
        """
        Hashes the password and the salt
        :return: hash
        """
        raise NotImplementedError()


class HashSHA256(IHash):

    def Hash(self, password: str, salt: str) -> str:
        h = hashlib.sha256()
        h.update((password + salt).encode())
        return h.hexdigest()


class HashSHA512(IHash):

    def Hash(self, password: str, salt: str) -> str:
        h = hashlib.sha512()
        h.update((password + salt).encode())
        return h.hexdigest()
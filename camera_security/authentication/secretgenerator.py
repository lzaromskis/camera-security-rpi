# secretgenerator.py | camera-security-rpi
# Implements the ISecretGenerator interface with SecretGenerator class
# Author: Lukas Žaromskis

import secrets
import string
from camera_security.authentication.isecretgenerator import ISecretGenerator


class SecretGenerator(ISecretGenerator):

    def __init__(self):
        pass

    def Generate(self, length: int) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))

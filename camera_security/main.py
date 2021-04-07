# main.py | camera-security-rpi
# Entry point
# Author: Lukas Žaromskis

from camera_security.program.camerasecurity import CameraSecurity
from camera_security.program.settings import Settings

if __name__ == '__main__':
    settings = Settings()
    cs = CameraSecurity()
    cs.Start(settings)

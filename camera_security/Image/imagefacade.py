# imagefacade.py | camera-security-rpi
# Describes the ImageFacade class for controlling the image getting and processing subsystem
# Author: Lukas Žaromskis


class ImageFacade:

    def __init__(self):
        self.camera_accessor = OpenCVCameraAccessor()
# settings.py | camera-security-rpi
# The settings class for loading program settings
# Author: Lukas Žaromskis

from os import path
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class Settings:

    PASSWORD_FILE_KEY = "password_file"
    HASH_METHOD_KEY = "hash_method"
    SECRET_GENERATION_METHOD_KEY = "secret_generation_method"
    LOGGER_TYPE_KEY = "logger_type"
    USE_TLS_KEY = "use_tls"
    TENSOR_MODEL_FILE_KEY = "tensor_model_file"
    TENSOR_LABELS_FILE_KEY = "tensor_labels_file"
    ACCEPTED_LABELS_KEY = "accepted_labels"
    CERTAINTY_THRESHOLD_KEY = "certainty_threshold"
    BOUNDS_RESIZE_PERCENTAGE_KEY = "bounds_resize_percentage"
    CAMERA_ID_KEY = "camera_id"
    MONITORED_ZONES_FILENAME_KEY = "monitored_zones_file"

    def __init__(self, settings_file=None):
        # Initialize dictionary with default values
        self.settings_dict = dict()
        self.settings_dict[self.PASSWORD_FILE_KEY] = "password.cspw"
        self.settings_dict[self.HASH_METHOD_KEY] = "sha256"
        self.settings_dict[self.SECRET_GENERATION_METHOD_KEY] = "secretgenerator"
        self.settings_dict[self.LOGGER_TYPE_KEY] = "console"
        self.settings_dict[self.USE_TLS_KEY] = "false"
        self.settings_dict[self.TENSOR_MODEL_FILE_KEY] = "detect.tflite"
        self.settings_dict[self.TENSOR_LABELS_FILE_KEY] = "coco_labels.txt"
        self.settings_dict[self.ACCEPTED_LABELS_KEY] = "person"
        self.settings_dict[self.CERTAINTY_THRESHOLD_KEY] = "0.6"
        self.settings_dict[self.BOUNDS_RESIZE_PERCENTAGE_KEY] = "0.1"
        self.settings_dict[self.CAMERA_ID_KEY] = "0"
        self.settings_dict[self.MONITORED_ZONES_FILENAME_KEY] = "zones.csmz"

        # If a file was given, read data from it
        if settings_file:
            self.__ReadSettings(settings_file)

    def __ReadSettings(self, filename: str):
        if not path.isfile(filename):
            raise FileNotFoundError("File \"" + filename + "\" does not exist!")

        f = open(filename, "r")
        while True:
            line = f.readline()
            if not line:
                break
            data = line.split('=')
            if len(data) != 2:
                continue
            # Only change existing keys. Do not add new keys
            if data[0] in self.settings_dict:
                self.settings_dict[data[0]] = data[1]

        f.close()

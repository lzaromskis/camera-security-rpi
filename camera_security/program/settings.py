# settings.py | camera-security-rpi
# The settings class for loading program settings
# Author: Lukas Žaromskis

from os import path
from typing import Optional

from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class Settings:
    PASSWORD_FILE_KEY = "password_file"
    HASH_METHOD_KEY = "hash_method"
    SECRET_GENERATION_METHOD_KEY = "secret_generation_method"
    LOGGER_TYPE_KEY = "logger_type"
    FILE_LOGGER_FILE_KEY = "file_logger_file"
    FILE_LOGGER_APPEND_KEY = "file_logger_append"
    USE_TLS_KEY = "use_tls"
    CERT_FILE_KEY = "cert"
    KEY_FILE_KEY = "key"
    TENSOR_MODEL_FILE_KEY = "tensor_model_file"
    TENSOR_LABELS_FILE_KEY = "tensor_labels_file"
    ACCEPTED_LABELS_KEY = "accepted_labels"
    CERTAINTY_THRESHOLD_KEY = "certainty_threshold"
    BOUNDS_RESIZE_COEFFICIENT_KEY = "bounds_resize_coefficient"
    CAMERA_ID_KEY = "camera_id"
    CAMERA_WIDTH_KEY = "camera_width"
    CAMERA_HEIGHT_KEY = "camera_height"
    MONITORED_ZONES_FILENAME_KEY = "monitored_zones_file"
    ALERTS_FOLDER_KEY = "alerts_folder"
    ALERTS_TO_KEEP_KEY = "alerts_to_keep"
    ALERT_TRIGGERED_TIMEOUT_SECONDS_KEY = "alert_triggered_timeout_seconds"

    def __init__(self, settings_file: Optional[str] = None):
        # Initialize dictionary with default values
        self.settings_dict = dict()
        self.settings_dict[self.PASSWORD_FILE_KEY] = "password.cspw"
        self.settings_dict[self.HASH_METHOD_KEY] = "sha256"
        self.settings_dict[self.SECRET_GENERATION_METHOD_KEY] = "secretgenerator"
        self.settings_dict[self.LOGGER_TYPE_KEY] = "console"
        self.settings_dict[self.FILE_LOGGER_FILE_KEY] = "camsec.log"
        self.settings_dict[self.FILE_LOGGER_APPEND_KEY] = "true"
        self.settings_dict[self.USE_TLS_KEY] = "false"
        self.settings_dict[self.CERT_FILE_KEY] = "cert.crt"
        self.settings_dict[self.KEY_FILE_KEY] = "key.key"
        self.settings_dict[self.TENSOR_MODEL_FILE_KEY] = "detect.tflite"
        self.settings_dict[self.TENSOR_LABELS_FILE_KEY] = "coco_labels.txt"
        self.settings_dict[self.ACCEPTED_LABELS_KEY] = "person"
        self.settings_dict[self.CERTAINTY_THRESHOLD_KEY] = "0.6"
        self.settings_dict[self.BOUNDS_RESIZE_COEFFICIENT_KEY] = "0.1"
        self.settings_dict[self.CAMERA_ID_KEY] = "0"
        self.settings_dict[self.CAMERA_WIDTH_KEY] = "640"
        self.settings_dict[self.CAMERA_HEIGHT_KEY] = "480"
        self.settings_dict[self.MONITORED_ZONES_FILENAME_KEY] = "zones.csmz"
        self.settings_dict[self.ALERTS_FOLDER_KEY] = "./alerts/"
        self.settings_dict[self.ALERTS_TO_KEEP_KEY] = "10"
        self.settings_dict[self.ALERT_TRIGGERED_TIMEOUT_SECONDS_KEY] = "30"

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
            data[0] = data[0].strip()
            data[1] = data[1].strip()
            # Only change existing keys. Do not add new keys
            if data[0] in self.settings_dict:
                self.settings_dict[data[0]] = data[1]
        f.close()

# emailalertaction.py | camera-security-rpi
# Implements the IAlertAction interface for sending an email to the client
# Author: Lukas Žaromskis

import smtplib
import ssl

from camera_security.monitoring.alerts.ialertaction import IAlertAction
from camera_security.utility.ilogger import ILogger


class EmailAlertAction(IAlertAction):

    MESSAGE = """\
    Subject: Alert
    
    The system received an alert!
    """

    def __init__(self, server_email_name: str, server_email_password: str, client_email_name: str, logger: ILogger):
        self.__server_name = server_email_name
        self.__server_pass = server_email_password
        self.__client_name = client_email_name
        self.__logger = logger

    def Execute(self, **kwargs):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.mail.com", 587, context=context) as server:
            server.login(self.__server_name, self.__server_pass)
            server.sendmail(self.__server_name, self.__client_name, self.MESSAGE)

# websocketmessages.py | camera-security-rpi
# Describes the messages the websocket can send and receive
# Author: Lukas Žaromskis


class WebsocketMessages:
    ALERT = "alert"
    CLOSE = "closing"
    PING = "ping"
    PONG = "pong"

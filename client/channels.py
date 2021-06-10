import socket
import time
import logging

from server_utils.hashing import hash_pw
from server_utils.signal import Signal

TIMEOUT_SEC = 5
logger = logging.getLogger("client")

class ServerDenial(BaseException):
    """Cannot connect to channel"""
    pass


class PasswordError(BaseException):
    """Channel is secured with password"""
    pass


class ChannelManager():
    def __init__(self, server_address, local_address):
        self.server_address = server_address
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.bind(local_address)
        self.soc.settimeout(TIMEOUT_SEC)
        self.port = None

    def ping(self) -> bool:
        try:
            message = Signal()
            message.code = b"PNG"

            self.soc.sendto(message.get_message(), self.server_address)
            returned, _ = self.soc.recvfrom(32)

            returned = Signal(returned)
            result = returned.code == b"PGR"

            logger.debug(f"Ping result: {result}")
            return result
        except socket.timeout:
            logger.warn("Pinging timed out")
            return False

    def disconnect_channel(self):
        self._send_disconnect_message()
        self.port = None
        self.clear_socket(self.soc)

    def connect_channel(self, channel: int, password=None) -> bool:
        try:
            if password is not None:
                self._send_secure_connect_message(channel, password)
            else:
                self._send_connect_message(channel)
            response, _ = self.soc.recvfrom(32)
            self._read_channel_connection_response(response)
        except socket.timeout:
            raise ServerDenial("Did not receive server response")

    def _send_disconnect_message(self):
        message = Signal()
        message.code = b"XXX"
        self.soc.sendto(message.get_message(), self.server_address)

    def _send_connect_message(self, channel: int):
        message = Signal()
        message.code = b"CON"
        message.two_byte = channel
        self.soc.sendto(message.get_message(), self.server_address)

    def _read_channel_connection_response(self, response: bytes) -> None:
        response = Signal(response)

        if response.code == b"DEN":
            raise ServerDenial("Server denied connection")
        if response.code == b"PRQ":
            raise PasswordError()
        if not response.code == b"ACC":
            msg = "Server sent invalid response"
            logger.warn(msg)
            raise ServerDenial(msg)

        if (port := int.from_bytes(response.two_byte, "big")) != 0:
            self.port = port
            logger.info(f"Audio port set to: {port}")

    def _send_secure_connect_message(self, channel: int, password: str):
        message = Signal()
        message.code = b"PAS"
        message.two_byte = channel
        message.rest = hash_pw(password.encode(), 27)
        self.soc.sendto(message.get_message(), self.server_address)

    @staticmethod
    def clear_socket(soc):
        try:
            while True:
                soc.recvfrom(1)
        except socket.timeout:
            pass

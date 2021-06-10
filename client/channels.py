import socket
import time
import logging

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
        raise TypeError("lolo")
        if password:
            return self._connect_securely(channel, password)
        return self._connect_channel(channel)

    def _send_disconnect_message(self):
        message = Signal()
        message.code = b"XXX"
        self.soc.sendto(message.get_message(), self.server_address)

    def _send_connect_message(self, channel: int):
        message = Signal()
        message.code = b"CON"
        message.two_byte = channel
        self.soc.sendto(message.get_message(), self.server_address)

    def _read_channel_connection_response(self, response: bytes) -> bool:
        response = Signal(response)

        if response.code == b"DEN":
            raise ServerDenial(msg)
        if response.code == b"PRQ":
            raise PasswordError()
        if not response.code == b"ACC":
            msg = "Server sent invalid response"
            logger.warn(msg)
            raise ServerDenial(msg)

        if (port := int.from_bytes(response.two_byte, "big")) != 0:
            self.port = port
            logger.info(f"Audio port set to: {port}")

        return True

    def _send_secure_connect_message(self, channel: int, password: str):
        message = Signal()
        message.code = "PAS"
        message.two_byte = channel
        message.password = hash_pw(password, 27)
        self.metadata_socket.sendto(message.get_message(), self.server_address)

    def _connect_channel(self, channel: int) -> bool:
        try:
            self._send_connect_message(channel)
            response, _ = self.soc.recvfrom(32)
            return self._read_channel_connection_response(response)
        except socket.timeout:
            return False

    def _connect_securely(self, channel: int, password: str) -> bool:
        try:
            self._send_secure_connect_message(channel, password)
            response, _ = self.soc.recvfrom(32)
            return self._read_channel_connection_response(response)
        except socket.timeout:
            return False

    @staticmethod
    def clear_socket(soc):
        try:
            while True:
                soc.recvfrom(1)
        except socket.timeout:
            pass

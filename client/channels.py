import socket
import time

from server_utils.signal import Signal

TIMEOUT_SEC = 5

class ConnetionError(BaseException):
    """Cannot connect to server"""
    pass


class PasswordError(BaseException):
    """Channel is secured with password"""
    pass


class ChannelManager():
    def __init__(self, server_address, local_address):
        self.server_address = server_address
        self.metadata_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.metadata_socket.bind(local_address)
        self.metadata_socket.settimeout(TIMEOUT_SEC)
        self.port = None

    def ping(self) -> bool:
        try:
            message = Signal()
            message.code = b"PNG"

            self.metadata_socket.sendto(message.get_message(), self.server_address)
            returned, server = self.metadata_socket.recvfrom(32)

            returned = Signal(returned)
            return returned.code == b"PGR"
        except socket.timeout:
            return False

    def disconnect_channel(self):
        self._send_disconnect_message()
        self.port = None
        self.clear_socket(self.metadata_socket)

    def connect_channel(self, channel: int, password=None) -> bool:
        if password is not None:
            return self._connect_securely(channel, password)
        return self._connect_channel(channel)

    def _send_disconnect_message(self):
        message = Signal()
        message.code = b"XXX"
        self.metadata_socket.sendto(message.get_message(), self.server_address)

    def _send_connect_message(self, channel: int):
        message = Signal()
        message.code = b"CON"
        message.two_byte = channel
        self.metadata_socket.sendto(message.get_message(), self.server_address)

    def _read_channel_connection_response(self, response: bytes) -> bool:
        response = Signal(response)
        if response.code == b"DEN":
            return False
        if response.code == b"PRQ":
            raise PasswordError()
        if not response.code == b"ACC":
            raise ConnectionError("Server sent invalid response")

        self.port = int.from_bytes(response.two_byte, "big")

        if self.port == 0:
            raise ConnectionError("Server send port 0!")

        return True

    def _send_secure_connect_message(self, channel: int, password: str):
        message = Signal()
        message.code = "PAS"
        message.two_byte = channel
        message.password = hash_pw(password)
        self.metadata_socket.sendto(message.get_message(), self.server_address)

    def _connect_channel(self, channel: int) -> bool:
        try:
            self._send_connect_message(channel)
            response, _ = self.metadata_socket.recvfrom(32)
            return self._read_channel_connection_response(response)
        except socket.timeout:
            return False

    def _connect_securely(self, channel: int, password: str) -> bool:
        try:
            self._send_secure_connect_message(channel, password)
            response, _ = self.metadata_socket.recvfrom(32)
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




def hash_pw(password: bytes) -> bytes:
    return b"2" * 27  # TODO

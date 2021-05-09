import socket

from signal_processing import Signal


class ConnetionError(BaseException):
    """Cannot connect to server"""
    pass


class PasswordError(BaseException):
    """Channel is secured with password"""
    pass


class ChannelManager():
    def __init__(self, server_address: str, server_port: int):
        self.server_address = (server_address, server_port)
        self.metadata_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def check_server(self):
        if not self.ping():
            raise ConnetionError()

    def ping(self) -> bool:  # TODO This does not work
        message = Signal()
        message.code = b"PNG"

        self.metadata_socket.sendto(message.get_message(), self.server_address)
        returned, server = self.metadata_socket.recvfrom(32)

        returned = Signal(returned)
        return returned.code == b"PGR"

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
        return True

    def _send_secure_connect_message(self, channel: int, password: str):
        message = Signal()
        message.code = "PASS"
        message.two_byte = channel
        message.password = hash_pw(password)
        self.metadata_socket.sendto(message.get_message(), self.server_address)

    def _connect_channel(self, channel: int) -> bool:
        self._send_connect_message(channel)
        response, _ = self.metadata_socket.recvfrom(32)
        return self._read_channel_connection_response(response)

    def _connect_securely(self, channel: int, password: str) -> bool:
        self._send_secure_connect_message(channel, password)
        response, _ = self.metadata_socket.recvfrom(32)
        return self._read_channel_connection_response(response)

    def connect_channel(
            self,
            channel: int,
            password=None) -> bool:  # TODO this does not work either
        if password is not None:
            return self._connect_securely(channel, password)
        return self._connect_channel(channel)


def hash_pw(password: bytes) -> bytes:
    return b"x" * 27  # TODO

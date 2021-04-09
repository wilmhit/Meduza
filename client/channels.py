import socket

# This is basic draft
# Make this work for now
# It doesn't need to change channels or talk to gui as of now


class ConnetionError(BaseException):
    """Cannot connect to server"""
    pass

class PasswordError(BaseException):
    """Channel is secured with password"""
    pass

def connect():
    connection = ConnectionManager("127.0.0.1", 50001)
    connection.connect_channel(1)
    # connection.connect_channel(user_selected_channel)
    # use pyAudio to open recording and listening streams
    # while True:
    # throw recv_audio_packet() to listening stream
    # throw send_audio_packet() to recording stream


class ConnectionManager():
    def __init__(self, server_address, server_port):
        self.server_address = (server_address, server_port)
        self.metadata_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not self.ping():
            raise

    def ping(self):
        fill = b"\0" * 29
        message = b"PNG" + fill
        self.metadata_socket.sendto(message, self.server_address)
        returned, server = self.metadata_socket.recvfrom(32)
        return returned == b"PGR" + fill

    def _send_connect_message(self, channel):
        channel_bytes = channel.to_bytes(2, "big")
        fill = b"\0" * 27
        message = b"CON" + channel_bytes + fill
        self.metadata_socket.sendto(message, self.server_address)

    def _connect_channel(self, channel):
        self._send_connect_message(channel)
        response, _ = self.metadata_socket.recvfrom(32)
        return self._read_channel_connection_response(response)

    def _read_channel_connection_response(self, response):
        if response.startswith(b"DEN"):
            return False
        if response.startswith(b"PRQ"):
            raise PasswordError()
        if not response.startswith(b"ACC"):
            raise ConnectionError("Server sent invalid response")
        return True

    def _connect_securely(self, channel, password):
        pass

    def connect_channel(self, channel: int, password=None) -> bool:
        if password is not None:
            return _connect_securely(channel, password)
        return _connect_channel(channel)

        return True
        ## ESTABLISHING AUDIO PORT
        # Send request from client metadata port to server metadata port
        # In request include channel you want to connect to
        # Server sends back audio port
        ## PUNCHING UDP HOLE
        # Idk how to solve this. Client needs to send packet to first.
        # Why? Server doesn't know what is client's audio port. You can't
        # just send port number. NAT might change it without client knowing
        # about it. Check wikipedia: UDP hole punching.

    def recv_audio_packet(self):
        # This method reads client audio port buffer
        # Will raise an error if used before connect_channel(channel)
        pass

    def send_audio_packet(self):
        # Same as above
        pass

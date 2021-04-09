import socket

# This is basic draft
# Make this work for now
# It doesn't need to change channels or talk to gui as of now


class ConnetionError(BaseException):
    """Cannot connect to server"""
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
        self.server_address = server_address
        self.server_port = server_port
        self.metadata_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not self.ping(server_address, server_port):
            raise

    def ping(self, ip, port):
        message = b"PING"
        self.metadata_socket.sendto(message, (ip, port))
        returned, server = self.metadata_socket.recvfrom(4)
        return returned == b"PONG"

    def connect_channel(self, channel):
        message = b"Hey, i want to connent to channel: " + bytes(str(channel), "UTF-8")
        self.metadata_socket.sendto(message, (self.server_address, self.server_port))
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

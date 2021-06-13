import logging
import socket

from server_utils.hashing import hash_pw
from server_utils.signal import Signal

from .channels import Channels
from .single_channel import SingleChannel

MAX_USERS_ON_CHANNEL = 3
logger = logging.getLogger("server")


class ClientManager:
    def __init__(self, ip, channels):
        self.IP_address = ip[0]
        self.IP_port = ip[1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))
        #self.acepted_cb = acepted_cb
        self.channels = channels

    def _send_message(self, code, channel, sender_data):
        message = Signal()
        message.code = bytes(code, encoding='utf-8')
        message.two_byte = channel
        self.sock.sendto(message.get_message(), sender_data)

    def con_signal(self, data_signal, sender_data):
        channel_number = int.from_bytes(data_signal.two_byte, "big")
        connected_users = self.channels.get_count_of_active_user(
            channel_number)

        if connected_users < MAX_USERS_ON_CHANNEL:
            port = self.channels.add_user_to_channel(channel_number,
                                                     sender_data)
            self._send_message("ACC", port, sender_data)
        else:
            self._send_message("DEN", None, sender_data)

    def pas_signal(self, data_signal, sender_data):
        channel_number = int.from_bytes(data_signal.two_byte, "big")
        connected_users = self.channels.get_count_of_active_user(
            channel_number)
        received_hash = data_signal.rest
        correct_hash = hash_pw(self.channels.channels[0]['password'].encode(), 27)

        if received_hash == correct_hash and connected_users < MAX_USERS_ON_CHANNEL:
            port = self.channels.add_user_to_channel(channel_number,
                                                     sender_data)
            self._send_message("ACC", port, sender_data)
        else:
            self._send_message("DEN", None, sender_data)

    def _read_signal(self, data):
        sender = data[1]
        data_signal = Signal(data[0])
        logger.debug(f"Received message with code: {data_signal.code}")

        if data_signal.code == b"CON":
            self.con_signal(data_signal, sender)
        elif data_signal.code == b"PNG":
            self._send_message("PGR", None, sender)
        elif data_signal.code == b"PAS":
            self.pas_signal(data_signal, sender)
        elif data_signal.code == b"XXX":
            self.channels.del_user_from_channel(sender)
        else:
            raise ConnectionError("Client send invalid signal")

        self.port = int.from_bytes(data_signal.two_byte, "big")

    def listen(self):
        logger.info("Server is now listening...")
        while True:
            data = self.sock.recvfrom(32)
            self._read_signal(data)


class Server:
    def __init__(self, ip_address, ip_port, channel_0_pass,
                 number_of_channels):
        #def acepted_cb(client_address, client_port):
        #    print("Client connected to channel")

        ip = (ip_address, ip_port)
        self.channels = Channels(channel_0_pass, number_of_channels, ip,
                                 SingleChannel)
        self.client_manager = ClientManager(ip, self.channels)

    def run(self):
        self.client_manager.listen()

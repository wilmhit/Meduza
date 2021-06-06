import socket
import time
from threading import Thread
from server_utils.signal import Signal
from .channels import Channels


class ClientManager:
    def __init__(self, ip, acepted_cb, channels):
        self.IP_address = ip[0]
        self.IP_port = ip[1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))
        self.acepted_cb = acepted_cb
        self.channels = channels

    def _send_message(self, code, channel, sender_data):
        message = Signal()
        message.code = bytes(code, encoding='utf-8')
        message.two_byte = channel
        self.sock.sendto(message.get_message(), sender_data)

    def _con_signal(self, data_signal, sender_data):
        channel_number = int.from_bytes(data_signal.two_byte, "big")

        if self.channels.get_count_of_active_user(channel_number) <= 5:
            port = self.channels.add_user_to_channel(channel_number,
                                            sender_data)
            self._send_message("ACC", port, sender_data)
        else:
            self._send_message("DEN", None, sender_data)

    def reply_ping(self, sender_ip):
        self._send_message("PGR", None, sender_ip)

    def _pas_signal(self, data_signal, sender_data):
        if data_signal.two_byte() == 0:
            if data_signal.rest() == self.channels.channels[0]['password']:
                self.channels.add_user_to_channel(data_signal.two_byte,
                                                sender_data)
                self._send_message("ACC", None, sender_data)
            else:
                self._send_message("DEN", None, sender_data)
        else:
            self._con_signal(data_signal, sender_data)

    def _xxx_signal(self, data_signal, sender_data):
        channel_number = int.from_bytes(data_signal.two_byte, "big")

        self.channels.del_user_from_channel(channel_number,
                                            sender_data[0], sender_data[1])

    def _read_signal(self, data):

        sender_ip = data[1]  # do przetestowania !
        data_signal = Signal(data[0])
        print("Received message with code: ", data_signal.code)
        if data_signal.code == b"CON":
            self._con_signal(data_signal, sender_ip)
        elif data_signal.code == b"PNG":
            self.reply_ping(sender_ip)
        elif data_signal.code == b"PAS":
            self._pas_signal(data_signal, sender_ip)
        elif data_signal.code == b"XXX":
            self._xxx_signal(data_signal, sender_ip)
        else:
            raise ConnectionError("Client send invalid signal")

        self.port = int.from_bytes(data_signal.two_byte, "big")


    def listen(self):
        print("Server is now listening...")
        while True:
            data = self.sock.recvfrom(32)
            self._read_signal(data)


class Server:
    def __init__(self, ip_address, ip_port, channel_0_pass,
                number_of_channels):
        def acepted_cb(client_address, client_port):
            print("Client connected to channel")

        ip = (ip_address, ip_port)
        self.channels = Channels(channel_0_pass, number_of_channels, ip)
        self.client_manager = ClientManager(ip, acepted_cb, self.channels)

    def run(self):
        self.client_manager.listen()

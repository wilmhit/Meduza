import socket
import time
from threading import Thread

from signal_processing import Signal

from .channels import Channels


class ClientManager:
    def __init__(self, IP_address, IP_port, acepted_cb, channels):
        self.IP_address = IP_address
        self.IP_port = IP_port
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
        if self.channels.get_count_of_active_user(data_signal.two_byte()) <= 5:
            self.channels.add_user_to_channel(data_signal.two_byte(),
                                              sender_data[0], sender_data[1])
            self._send_message("ACC", None, sender_data)
        else:
            self._send_message("DEN", None, sender_data)

    def _png_signal(self, data_signal, sender_data):
        self._send_message("PGR", None, sender_data)

    def _pas_signal(self, data_signal, sender_data):
        if data_signal.two_byte() == 0:
            if data_signal.rest() == self.channels.channels[0]['password']:
                self.channels.add_user_to_channel(data_signal.two_byte(),
                                                  sender_data[0],
                                                  sender_data[1])
                self._send_message("ACC", None, sender_data)
            else:
                self._send_message("DEN", None, sender_data)
        else:
            self._con_signal(data_signal, sender_data)

    def _xxx_signal(self, data_signal, sender_data):
        self.channels.del_user_from_channel(data_signal.two_byte(),
                                            sender_data[0], sender_data[1])

    def _read_signal(self, data):

        sender_data = data[1]  # do przetestowania !
        data_signal = Signal(data[0])
        if data_signal.code == b"CON":
            self._con_signal(data_signal, sender_data)
        if data_signal.code == b"PNG":
            self._png_signal(data_signal, sender_data)
        if data_signal.code == b"PAS":
            self._pas_signal(data_signal, sender_data)
        if data_signal.code == b"XXX":
            self._xxx_signal(data_signal, sender_data)
        else:
            raise ConnectionError("Client send invalid signal")

        self.port = int.from_bytes(data_signal.two_byte, "big")

    def test_add(self):
        self.channels.add_user_to_channel(1, "127.0.0.1", 50010)
        self.channels.add_user_to_channel(2, "127.0.0.1", 50011)
        self.channels.add_user_to_channel(4, "127.0.0.1", 50012)
        time.sleep(3)
        print(self.channels.get_list_users_on_chanel(1))
        self.channels.del_user_from_channel(2, "127.0.0.1", 50011)
        print(self.channels.get_list_users_on_chanel(1))
        time.sleep(3)
        self.channels.add_user_to_channel(2, "127.0.0.1", 50011)

    def listen(self):
        print("listen method - ON\n")
        self.test_add()
        #while True:
        #    data = self.sock.recvfrom(32) #buffer size is 1024 bytes 0 - data, 1 IP [0] / PORT [1]
        #    print("received message: %s" % data[0])
        #    self._read_signal(data)


class Server:
    def __init__(self, ip_address, ip_port, channel_0_pass,
                 number_of_channels):
        def acepted_cb(client_address, client_port):
            print("Client connected! :)")

        self.main_ip_port = ip_port
        self.main_ip_address = ip_address

        self.channels = Channels(channel_0_pass, number_of_channels,
                                 self.main_ip_port, self.main_ip_address)
        self.client_manager = ClientManager(self.main_ip_address,
                                            self.main_ip_port, acepted_cb,
                                            self.channels)

    def run(self):
        self.client_manager.listen()

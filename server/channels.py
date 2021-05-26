from random import randint
from threading import Thread

from .single_channel import SingleChannel

PORT_MIN = 50100
PORT_MAX = PORT_MIN + 500
NUMBER_OF_CHANNELS = 10


class Channels:
    def __init__(self, channel_0_pass: str, ip_port: int, ip_address: str):
        self.main_ip_port = ip_port
        self.main_ip_address = ip_address

        self.channels = [{
            "port": PORT_MIN,
            "password": channel_0_pass,
            "connected_users": [],
            "thread": None
        }]

        for num in range(1, NUMBER_OF_CHANNELS):
            self.create_channel(num)

        print("channels dict has been created")

    def create_channel(self, channel_num):
        if channel_num not in self.channels:
            self.channels.append({
                "port": self.get_port_num(),
                "password": None,
                "connected_users": [],
                "thread": None
            })

    def get_port_num(self):
        port = randint(PORT_MIN, PORT_MAX)
        while self.used(port):
            port = randint(PORT_MIN, PORT_MAX)

        return port

    def used(self, port):
        if port == self.main_ip_port:
            return True

        for chan in self.channels:
            if chan['port'] == port:
                return True

        return False

    def add_user_to_channel(self, channel_number, user_address) -> int:

        if not self.channels[channel_number]['connected_users']:
            self.channels[channel_number]['thread'] = SingleChannel(
                channel_number,
                (self.main_ip_address[0], self.channels[channel_number]['port']))
            self.channels[channel_number]['thread'].start()

        self.channels[channel_number]['connected_users'].append(user_address)
        return self.channels[channel_number]['port']

    def del_user_from_channel(self, channel_number, userIP, userPort):

        if self.channels[channel_number]['connected_users']:
            self.channels[channel_number]['thread'].set_stop_value()
            self.channels[channel_number]['thread'] = None

        user = (userIP, userPort)
        self.channels[channel_number]['connected_users'].remove(user)

    def get_count_of_active_user(self, channel_number):
        return len(self.channels[channel_number]['connected_users'])

    def get_list_users_on_chanel(self, channel_number):
        return self.channels[channel_number]['connected_users']

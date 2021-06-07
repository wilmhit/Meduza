from random import randint
from threading import Thread, ThreadError

from .single_channel import SingleChannel

PORT_MIN = 50100
PORT_MAX = PORT_MIN + 500
NUMBER_OF_CHANNELS = 10


class Channels:
    def __init__(self, channel_0_pass: str, ip_port: int, ip_address: str, ThreadClass):
        self.main_ip_port = ip_port
        self.main_ip_address = ip_address
        self.ThreadClass = ThreadClass

        self.channels = [{
            "port": PORT_MIN,
            "password": channel_0_pass,
            "connected_users": [],
            "thread": None
        }]

        for num in range(1, NUMBER_OF_CHANNELS):
            self.create_channel(num)

    def create_channel(self, channel_num):
        port = self.get_port_num()

        if channel_num not in self.channels:
            self.channels.append({
                "port": port,
                "password": None,
                "connected_users": [],
                "thread": None
            })

            channel_ip = (self.main_ip_address[0], port)
            thread = self.ThreadClass(channel_num,
                                    channel_ip, 
                                    self.channels[channel_num]['connected_users'])

            self.channels[channel_num]["thread"] = thread
        

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
        channel_dict =  self.channels[channel_number]

        if not channel_dict['connected_users']:
            channel_dict['thread'].start()

        channel_dict['connected_users'].append(user_address)
        return channel_dict['port']

    def del_user_from_channel(self, channel_number, user_address):
        channel_dict =  self.channels[channel_number]
        channel_dict['connected_users'].remove(user_address)

        if len(channel_dict['connected_users']) == 0:
            channel_dict['thread'].stop()

    def get_count_of_active_user(self, channel_number):
        return len(self.channels[channel_number]['connected_users'])

    def get_list_users_on_chanel(self, channel_number):
        return self.channels[channel_number]['connected_users']

from random import randint

PORT_MIN = 50100
PORT_MAX = PORT_MIN + 500

class Channels:
    def __init__(self, channel_0_pass, number_of_channels, ip_port, ip_address):

        self.main_ip_port = ip_port
        self.main_ip_address = ip_address
        
        self.channels = {
            0:{
                "port": PORT_MIN,
                "password": channel_0_pass,
                "connected_users":[]   
            }
        }
        for num in range(1, number_of_channels):
            self.create_channel(num)

        print("channels dict has been created")

    def create_channel(self, channel_num):
        if channel_num not in self.channels:
            self.channels[channel_num] = {
                "port":self.get_port_num(),
                "password":None,
                "connected_users":[]
            }

    def get_port_num(self):
        port = randint(PORT_MIN, PORT_MAX)
        while self.used(port):
            port = randint(PORT_MIN, PORT_MAX)
        
        return port

    def used(self, port):
        if port == self.main_ip_port:
            return True

        for chan in self.channels.keys():
            if self.channels[chan]['port'] == port:
                return True

        return False


    def add_user_to_channel(self, channel_number, userIP, userPort):
        user = {
            "IP": userIP,
            "Port": userPort
        }
        self.channels[channel_number]['connected_users'].append(user)
        pass

    def del_user_from_channel(self, channel_number, userIP, userPort):
        user = {
            "IP": userIP,
            "Port": userPort
        }
        self.channels[channel_number]['connected_users'].remove(user)
        pass

    def get_count_of_active_user(self, channel_number):
        return len(self.channels[channel_number]['connected_users'])

    def get_list_users_on_chanel(self, channel_number):
        return self.channels[channel_number]['connected_users']



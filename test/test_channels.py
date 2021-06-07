import unittest
from server.single_channel import mock_SingleChannel
from server.channels import Channels
import time

class TestChannels(unittest.TestCase):
    
    def setUp(self):
        # TODO create client manager here
        ip = ("127.0.0.1", 50001)
        self.channels = Channels("zaq1", 5, ip, mock_SingleChannel)
        #self.clients = ClientManager(ip, self.channels)

    def test_adding(self):
        self.channels.add_user_to_channel(1, ("127.0.0.1", 50010))
        self.channels.add_user_to_channel(2, ("127.0.0.1", 50011))
        self.channels.add_user_to_channel(4, ("127.0.0.1", 50012))
        #self.assertEqual()
        self.channels.del_user_from_channel(2, ("127.0.0.1", 50011))
        self.channels.add_user_to_channel(3, ("127.0.0.1", 50011))

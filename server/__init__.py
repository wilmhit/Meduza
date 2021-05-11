import socket
from threading import Thread
from .voip_server import Server, ClientManager
from server_utils.echo import EchoServer


UDP_IP = "127.0.0.1"
UDP_PORT = 50001
PASSWORD = "pass"
NUM_OF_CHANNELS = 10

def main():
    server = Server(UDP_IP, UDP_PORT, PASSWORD, NUM_OF_CHANNELS)
    server.run()
    #rec_thr = Thread(target=Server.listen)
    #rec_thr.start()

def mock_main():
    #server = Server(UDP_IP, UDP_PORT, PASSWORD, NUM_OF_CHANNELS)
    echo_server = EchoServer((UDP_IP, UDP_PORT))
    echo_server.start()

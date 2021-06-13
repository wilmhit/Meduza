from threading import Thread
from logging import DEBUG, INFO
import logging
from .voip_server import Server, ClientManager
from server_utils.echo import EchoServer
from server_utils.logger import create_logger

from .voip_server import Server

UDP_IP = "0.0.0.0"
UDP_PORT = 50001
PASSWORD = "pass"
NUM_OF_CHANNELS = 10


def main():
    logger = create_logger("server", DEBUG)
    logger.info("Starting server")

    server = Server(UDP_IP, UDP_PORT, PASSWORD, NUM_OF_CHANNELS)
    server.run()
    #rec_thr = Thread(target=Server.listen)
    #rec_thr.start()

def mock_main():
    #server = Server(UDP_IP, UDP_PORT, PASSWORD, NUM_OF_CHANNELS)
    echo_server = EchoServer((UDP_IP, UDP_PORT))
    echo_server.start()

import socket
import time
from threading import Thread
from server_utils.abstract import BaseServer
from typing import Any


class SingleChannel(BaseServer):
    def __init__(self, channel_num, ip) -> None:
        self.channel_num = channel_num
        self.ip = ip

    def _main_loop(self, socket) -> None:
        print("I'm a thread! :) number: ", self.channel_num)
        # TO DO -> nasłuchiwanie na sokocie oraz obsługa / przekazywanie do pozostałych
        time.sleep(1)

    def _thread_local(self) -> tuple[Any]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.ip)
        return (sock, )

import socket
import time
from threading import Thread
from server_utils.abstract import BaseServer
from typing import Any, Tuple


CHUNK = 4249

class SingleChannel(BaseServer):
    def __init__(self, channel_num, ip:Tuple[str, int], connected_users) -> None:
        self.channel_num = channel_num
        self.ip = ip
        self.connected_users = connected_users

    @classmethod
    def _main_loop(self, socket, connected_users) -> None:

        received_packets = []
        try:
            while True:
                data, user = socket.recvfrom(CHUNK)
                received_packets.append((data, user))
        except BlockingIOError: ...

        #print(received_packets)
        if len(received_packets) > 0:
            self.send_audio(received_packets[0][0], connected_users, socket)
        else:
            time.sleep(0.01)
        # TO DO -> nasłuchiwanie na sokocie oraz obsługa / przekazywanie do pozostałych

    @staticmethod
    def send_audio(receive, connected_users, socket):
        for user in connected_users:
            socket.sendto(receive, user)
    

    def _thread_local(self) -> Tuple[Any]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.ip)
        sock.bind(self.ip)
        sock.setblocking(False)
        return (sock, self.connected_users)

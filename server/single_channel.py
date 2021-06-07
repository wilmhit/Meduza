import socket
import time
from threading import Thread
from server_utils.abstract import BaseServer
from server_utils.inactivity import InactivityStore
from typing import Any, Tuple


CHUNK = 4249

class SingleChannel(BaseServer):
    def __init__(self, channel_num, ip:Tuple[str, int], connected_users) -> None:
        self.channel_num = channel_num
        self.ip = ip
        self.connected_users = connected_users

    @classmethod
    def _main_loop(cls, socket, connected_users, inactivity_store) -> None:
        received_packets = []
        try:
            while True:
                data, user = socket.recvfrom(CHUNK)
                received_packets.append((data, user))
        except BlockingIOError: ...


        if len(received_packets) > 0:
            cls.register_inactivities(inactivity_store, received_packets,
                                    connected_users)
            for user in inactivity_store.inactive_keys:
                print(f"Kicked user: {user}")
                connected_users.remove(user)
                inactivity_store.remove_key(user)

            cls.send_audio(received_packets[0][0], connected_users, socket)
        else:
            time.sleep(0.01)

    @staticmethod
    def register_inactivities(store, packets, users):
        _, active_users = zip(*packets)
        inactive_users = [user for user in users if user not in active_users]
        store.register_inactivity(inactive_users)

    @staticmethod
    def send_audio(receive, connected_users, socket):
        for user in connected_users:
            socket.sendto(receive, user)

    def _thread_local(self) -> Tuple[Any]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.ip)
        sock.setblocking(False)

        return (sock, self.connected_users, InactivityStore())
        return (sock, self.connected_users)


class mock_SingleChannel(BaseServer):
    def __init__(*args) -> None:
        pass

    @classmethod
    def _main_loop(*args) -> None:
        time.sleep(0.5)

    def _thread_local(self) -> Tuple[Any]:
        pass


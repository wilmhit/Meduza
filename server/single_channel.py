import socket
import time
from threading import Thread
from server_utils.abstract import BaseServer
from server_utils.inactivity import InactivityStore
from typing import Any, Tuple
from server_utils.audio_merge import audioMerge
import pickle
import logging
from client.voip import AudioStreams

logger = logging.getLogger("server")


CHUNK = 4249

class SingleChannel(BaseServer):

    temp_audio_packets = []

    def __init__(self, channel_num, ip:Tuple[str, int], connected_users) -> None:
        self.channel_num = channel_num
        self.ip = ip
        self.connected_users = connected_users

    @classmethod
    def _main_loop(cls, socket, connected_users, inactivity_store) -> None:
        received_packets = []
        try:
            while True:
                received_packets.append(socket.recvfrom(CHUNK))
        except BlockingIOError: ...

        if len(received_packets) > 0:

            if len(cls.temp_audio_packets) > 200:
                print("Started playback")
                stream = AudioStreams()
                for packet in cls.temp_audio_packets:
                    stream.play(packet)
                cls.temp_audio_packets = []

            mergeAudio = audioMerge(received_packets)

            for user in connected_users:
                audio_pck = mergeAudio.get_audio_for_user(user)
                if user == connected_users[0]:
                    cls.temp_audio_packets.append(audio_pck)
                cls.send_audio(audio_pck, socket, user)

            cls.register_inactivities(inactivity_store, received_packets,
                                    connected_users)
            for user in inactivity_store.inactive_keys:
                logger.debug(f"Kicked user: {user}")
                connected_users.remove(user)
                inactivity_store.remove_key(user)

    @staticmethod
    def register_inactivities(store, packets, users):
        _, active_users = zip(*packets)
        inactive_users = [user for user in users if user not in active_users]
        store.register_inactivity(inactive_users)

    @staticmethod
    def send_audio(receive, socket, user):
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


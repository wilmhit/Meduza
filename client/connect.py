import time
from threading import Thread
from typing import Dict, Optional, Tuple, Any

from .channels import ConnectionManager
from .gui_callbacks import gui_state as shared_vars
from .voip import VoipClient

UPDATE_INTERVAL = 1

class ConnectionManager():
    def __init__(self, shared_vars: Dict[str, Any]):
        self.shared_vars = shared_vars

    def get_connected_channel(self) -> Optional[int]:
        for channels in enumerate(self.shared_vars["channels"]):
            pass
            # TODO if connected return id
        return None

    def read_server_address(self) -> Tuple[str, int]:
        # TODO Return whatever is in shared_vars["server_ip"]
        return "127.0.0.1", 50001

    def watch_channels(self):
        connected_channel = self.get_connected_channel()
        if get_connected_channel() is not None:
            print("Connecting to channel")
            self.connection.connect_channel(connected_channel)
            voip_client = VoipClient(self.server_ip_tuple[0], connection.port)
            voip_client.loop_while(shared_vars)

    def connect(self):
        print("Trying to connect to provided IP")
        self.server_ip_tuple = self.read_server_address()
        self.connection = ConnectionManager(*server_ip_tuple)
        self.shared_vars["connected"] = connection.check_sever()
        while self.shared_vars["connected"]:
            self.watch_channels()
            print("Watching for channels")
        time.sleep(UPDATE_INTERVAL)

    def main_loop(self):
        while True: # TODO while window is not destroyed
            if self.shared_vars["server_ip"] != "":
                self.connect()
            print("Waiting for server IP")
            time.sleep(UPDATE_INTERVAL)

import time
from threading import Thread
from typing import Dict, Optional, Tuple, Any

from .channels import ChannelManager
from .gui_callbacks import gui_state as shared_vars
from .voip import VoipClient

UPDATE_INTERVAL = 1

class ConnectionManager():
    def __init__(self, shared_vars: Dict[str, Any]):
        self.shared_vars = shared_vars

    def get_connected_channel(self) -> Optional[int]:
        for channel_id, channel in enumerate(self.shared_vars["channels"]):
            if channel["connected"] == True:
                return channel_id
        return None

    def read_server_address(self) -> Tuple[str, int]:
        # TODO Return whatever is in shared_vars["server_ip"]
        return "127.0.0.1", 50001

    def watch_channels(self):
        connected_channel = self.get_connected_channel()
        if self.get_connected_channel() is not None:
            print("Connecting to channel")
            # self.connection.connect_channel(connected_channel) TODO fix
            self.connection.port = 1515 # TODO Delete once ChannelManager is fixed
            # TODO handle channel denied
            voip_client = \
                VoipClient(self.server_ip_tuple[0], self.connection.port)
            voip_client.loop_while(shared_vars)

    def connect(self):
        print("Trying to connect to provided IP")
        self.server_ip_tuple = self.read_server_address()
        self.connection = ChannelManager(*self.server_ip_tuple)
        self.shared_vars["connection_validated"] = True #self.connection.check_server()
        while self.shared_vars["connection_validated"]:
            self.watch_channels()
            print("Watching for channels")
            time.sleep(UPDATE_INTERVAL)

    def main_loop(self):
        while self.shared_vars["is_running"]:
            if self.shared_vars["server_ip"] != "":
                self.connect()
            print("Waiting for server IP")
            time.sleep(UPDATE_INTERVAL)

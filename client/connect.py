import time
from threading import Thread
from typing import Any, Dict, Optional, Tuple

from .channels import ChannelManager
from .gui_callbacks import gui_state as shared_vars
from .voip import VoipClient

from server_utils.abstract import BaseServer

UPDATE_INTERVAL = 1


class ConnectionManager(BaseServer):
    def __init__(self, shared_vars: Dict[str, Any],
                 local_address: Tuple[str, int]):
        self.shared_vars = shared_vars
        self.local_address = local_address

    def _main_loop(self):
        self._running = self.shared_vars["is_running"]
        self.connect()
        time.sleep(UPDATE_INTERVAL)

    def connect(self):
        address = self.read_server_address()
        if not address:
            return

        if self.__validate_connection(address):
            self.watch_channels()

    def watch_channels(self):
        channel = self.get_selected_channel()
        if type(channel) == int and self.connection.connect_channel(channel):
            client = VoipClient(self.server_ip_tuple[0],self.connection.port)
            client.loop_while(shared_vars)

    def get_selected_channel(self) -> Optional[int]:
        for channel_id, channel in enumerate(self.shared_vars["channels"]):
            if channel["connected"] == True:
                return channel_id
        return None

    def read_server_address(self) -> Optional[Tuple[str, int]]:
        try:
            ip, port = shared_vars["server_ip"].split(":")
            return ip, int(port)
        except ValueError:
            return None

    def __validate_connection(self, address) -> bool:
        if self.shared_vars["connection_validated"]:
            return True

        self.connection = self.make_connection(address, self.local_address)
        if self.connection:
            self.shared_vars["connection_validated"] = True
        return bool(self.connection)

    @staticmethod
    def make_connection(server_address, local_address) -> Optional[ChannelManager]:
        connection = ChannelManager(server_address, local_address)
        if connection.ping():
            return connection
        else:
            return None

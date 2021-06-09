import time
from socket import timeout as SocketTimeoutException
from threading import Thread
from typing import Any, Dict, Optional, Tuple

from .channels import ChannelManager
from .gui_callbacks import gui_state as shared_vars
from .voip import VoipClient

from server_utils.abstract import BaseServer
from logging import getLogger

UPDATE_INTERVAL = 1
logger = getLogger("client")


class ConnectionManager(BaseServer):  # TODO refactor
    def __init__(self, shared_vars: Dict[str, Any], local_address: Tuple[str, int]):
        self.shared_vars = shared_vars
        self.local_address = local_address
        self.connection = None

    def _main_loop(self):
        self._running = self.shared_vars["is_running"]
        self.connect()
        time.sleep(UPDATE_INTERVAL)

    def connect(self):
        address = self.read_server_address()
        if not address:
            return

        if self.__validate_connection(address):
            self.server_ip = address
            self.watch_channels()

    def watch_channels(self):
        channel = self.get_selected_channel()
        if type(channel) == int and self.connection.connect_channel(channel):
            try:
                voip_address = self.server_ip[0], self.connection.port
                client = VoipClient(voip_address,
                                    self.connection.metadata_socket)
                client.loop_while(shared_vars)
            except SocketTimeoutException:
                logger.warn("Lost connection during VOIP")
                self.shared_vars["connection_validated"] = False
            self.connection.disconnect_channel()
            self.shared_vars["disconnect_channel"]()

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

        if not self.connection:
            self.connection = self.make_connection(address, self.local_address)

        if self.connection:
            self.shared_vars["connection_validated"] = True
        else:
            logger.warn("Could not reach server")
            self.shared_vars["server_ip"] = ""
        return bool(self.connection)

    @staticmethod
    def make_connection(server_address,
                        local_address) -> Optional[ChannelManager]:
        connection = ChannelManager(server_address, local_address)
        if connection.ping():
            return connection
        else:
            return None

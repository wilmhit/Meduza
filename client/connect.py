import time
from socket import timeout as SocketTimeoutException
from threading import Thread
from typing import Any, Dict, Optional, Tuple

from .channels import ChannelManager, ServerDenial, PasswordError
from .gui_callbacks import gui_state as shared_vars
from .voip import VoipClient

from server_utils.abstract import BaseServer
from logging import getLogger

UPDATE_INTERVAL = 1
logger = getLogger("client")


class ConnectionManager(BaseServer):
    def __init__(self, shared_vars: Dict[str, Any], local_address: Tuple[str, int]):
        self.shared_vars = shared_vars
        self.local_address = local_address
        self.connection = None

    def _main_loop(self):
        time.sleep(UPDATE_INTERVAL)

        if not self.shared_vars["is_running"]:
            logger.debug("Detected stop condition")
            self._running = False

        self.server_address = self.read_server_address()
        if not self.server_address:
            return

        if not self.connection:
            self.connection = self.make_connection(self.server_address,
                                                   self.local_address)
            logger.debug("Waiting for connection")
            return

        self.shared_vars["connection_validated"] = True
        channel = self.get_selected_channel()
        if type(channel) != int:
            logger.debug("Waiting for channel selection")
            return

        try:
            self.connect_to_channel(channel)
            self.connection.disconnect_channel()
        except SocketTimeoutException:
            logger.warn("Connection lost")
            self.shared_vars["connection_validated"] = False
            self.connection = None
            self.shared_vars["server_ip"] = ""
            self.shared_vars["disconnect_channel"]()
        except PasswordError:
            logger.warn("Tried connecting to password protected channel")
            self.shared_vars["disconnect_channel"]()
        except ServerDenial:
            logger.warn("Server refused connection")
            self.shared_vars["disconnect_channel"]()

    def connect_to_channel(self, channel):
        if channel == 0:
            self.connection.connect_channel(channel, password=self.shared_vars["password"])
        else:
            self.connection.connect_channel(channel)
        voip_address = self.server_address[0], self.connection.port
        client = VoipClient(voip_address, self.connection.soc)
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

    @staticmethod
    def make_connection(server_address,
                        local_address) -> Optional[ChannelManager]:
        connection = ChannelManager(server_address, local_address)
        if connection.ping():
            return connection
        else:
            return None

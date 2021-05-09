import time
from typing import Any, Dict


class VoipClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        # TODO here create audio streams
    
    def loop_while(self, shared_vars: Dict[str, Any]):
        while (variable_set["channel_connected"]):

            if variable_set["mute_mic"]:
                self.send_dummy_audio()
            else:
                self.send_audio()

            if variable_set["mute_spk"]:
                self.receive_dummy_audio()
            else:
                self.receive_audio()
            

    # Use audio streams in methods below
    def send_audio(self):
        pass

    def send_dummy_audio(self):
        pass

    def receive_dummy_audio(self):
        pass
    
    def receive_audio(self):
        pass

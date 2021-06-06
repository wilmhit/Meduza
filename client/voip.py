import time
from typing import Any, Dict
import sounddevice as sd
import pickle

CHUNK = 1024 * 4
CHANNELS = 1
RATE = 44100

# How many seconds of audio fits into one chunk?
SECONDS_AUDIO = CHUNK // (RATE // 8) 

class VoipClient:
    def __init__(self, server_address, soc):
        self.server_address = server_address
        self.soc = soc
        self.audio = AudioStreams()

    def loop_while(self, shared_vars: Dict[str, Any]):
        while (shared_vars["channel_connected"]):

            if shared_vars["mute_mic"]:
                self.send_dummy_audio()
            else:
                self.send_audio()

            if shared_vars["mute_spk"]:
                self.receive_dummy_audio()
            else:
                self.receive_audio()

    def send_audio(self):
        audio = self.audio.record()
        self.soc.sendto(audio, self.server_address)

    def send_dummy_audio(self):
        dummy_audio = int(0).to_bytes(CHUNK, "big")
        self.soc.sendto(dummy_audio, self.server_address)

    def receive_dummy_audio(self):
        data, client = self.soc.recvfrom(CHUNK)

    def receive_audio(self):
        data, client = self.soc.recvfrom(CHUNK)
        self.audio.play(data)


import time
from typing import Any, Dict

CHUNK = 4096

class VoipClient:
    def __init__(self, server_address, soc):
        self.server_address = server_address
        self.soc = soc
        self.audio = AudioStreams()

    def loop_while(shared_vars: Dict[str, Any]):
        while (shared_vars["channel_connected"]):

            if shared_vars["mute_mic"]:
                self.send_dummy_audio(server, soc)
            else:
                self.send_audio(server, server, soc)

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
        data, client = soc.recvfrom(CHUNK)

    def receive_audio(self):
        data, client = soc.recvfrom(CHUNK)
        self.audio.play(data)

class AudioStreams:
    def __init__(self):
        stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)

    def record(self) -> bytes:
        return int(0).to_bytes(CHUNK, "big")

    def play(self, audio: bytes):
        pass

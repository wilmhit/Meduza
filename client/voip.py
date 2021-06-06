import time
from typing import Any, Dict
import pickle
import pyshine

CHUNK = 1024 * 4
CHANNELS = 1
RATE = 44100

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
        data, client = soc.recvfrom(CHUNK)

    def receive_audio(self):
        data, client = soc.recvfrom(CHUNK)
        self.audio.play(data)

class AudioStreams:
    def __init__(self):
        self.recording_stream, _ = pyshine.audioCapture(mode="send")
        self.playback_stream, _ = pyshine.audioCapture(mode="get")

    def record(self) -> bytes:
        audio = self.recording_stream.get()
        return pickle.dumps(audio)

    def play(self, audio: bytes):
        audio_frame = picke.loads(audio)
        self.playback_stream.put(audio_frame)

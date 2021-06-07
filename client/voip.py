import time
from typing import Any, Dict
import sounddevice as sd
import pickle

CHUNK = 1024 * 4
CHANNELS = 1
RATE = 44100

# How many seconds of audio fits into one chunk?
SECONDS_AUDIO = CHUNK / (RATE * 4)


class VoipClient:
    def __init__(self, server_address, soc):
        self.server_address = server_address
        self.soc = soc
        self.audio = AudioStreams()
        self.packet_size = len(self.audio.record_dummy())

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
        dummy_audio = self.audio.record_dummy()
        self.soc.sendto(dummy_audio, self.server_address)

    def receive_dummy_audio(self):
        data, client = self.soc.recvfrom(self.packet_size)

    def receive_audio(self):
        data, client = self.soc.recvfrom(self.packet_size)
        self.audio.play(data)


class AudioStreams:
    def __init__(self):
        sd.default.samplerate = RATE
        sd.default.channels = 1
        self.stream = sd.Stream()
        self.stream.start()
        self.dummy_record, _ = self.stream.read(self.frames_in_chunk)

    def record_dummy(self):
        self.stream.read(self.frames_in_chunk)
        return pickle.dumps(self.dummy_record)

    @property
    def frames_in_chunk(self):
        return int(SECONDS_AUDIO * RATE)

    def record(self):
        audio, _ = self.stream.read(self.frames_in_chunk)
        return pickle.dumps(audio)

    def play(self, audio):
        self.stream.write(pickle.loads(audio))

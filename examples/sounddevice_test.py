import time
from typing import Any, Dict
import sounddevice as sd
import pickle

CHUNK = 1024 * 4
CHANNELS = 1
RATE = 44100

# How many seconds of audio fits into one chunk?
SECONDS_AUDIO = CHUNK / (RATE * 4)

class AudioStreams:

    def __init__(self):
        sd.default.samplerate = RATE
        sd.default.channels = 1
        self.stream = sd.Stream()
        self.stream.start()
        self.last_received = self.stream.read(self.frames_in_chunk)

    @property
    def frames_in_chunk(self):
        return int(SECONDS_AUDIO * RATE)

    def record(self):
        audio, _ = self.stream.read(self.frames_in_chunk)
        return pickle.dumps(audio)

    def play(self, audio):
        self.stream.write(pickle.loads(audio))

streams = AudioStreams()
i = 0
while True:
    i += 1
    audio = streams.record()
    streams.play(audio)
    print(len(audio))
    print(i)

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
        return audio

    def play(self, audio):
        self.stream.write(audio)

streams = AudioStreams()
i = 0

fragments1, fragments2 = [], []
print("record start")

for x in range(500):
    fragments1.append(streams.record())

print("koniec 1")

for x in range(500):
    fragments2.append(streams.record())

print("koniec 2")

all_rec = []

for x in range(len(fragments1)):
    all_rec.append(fragments1[x] + fragments2[x])
    
for x in all_rec:
    streams.play(x)

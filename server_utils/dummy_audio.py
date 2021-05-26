from .abstract import BaseServer
import socket
import time

TIMEOUT_SEC = 1
INTERVAL = .05
CHUNK = 4096

class DummyAudioClient(BaseServer):
    def __init__(self, address, server_address, chunk_size=1024, soc=None):
        self.address = address
        self.chunk_size = chunk_size
        self.socket = soc
        self.server_address = server_address

    def _thread_local(self):
        if self.socket is None:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.bind(self.address)
        else:
            soc = self.socket
        soc.settimeout(TIMEOUT_SEC)
        soc.setblocking(False)
        dummy_audio = int(0).to_bytes(CHUNK, "big")
        return (soc, dummy_audio, self.server_address)

    def _main_loop(self, soc, audio, server):
        try:
            soc.sendto(audio, server)

            try:
                data, ip = soc.recvfrom(self.chunk_size)
                print(f"Received {data} back from {ip}")
            except BlockingIOError: ...

            time.sleep(INTERVAL)
        except socket.timeout:
            print("Timed out while waiting for data")

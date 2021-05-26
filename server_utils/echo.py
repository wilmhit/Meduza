from .abstract import BaseServer
import socket

TIMEOUT_SEC = 1

class EchoServer(BaseServer):
    def __init__(self, address, chunk_size=1024, soc=None):
        self.address = address
        self.chunk_size = chunk_size
        self.socket = soc

    def _thread_local(self):
        if self.socket is None:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.bind(self.address)
        else:
            soc = self.socket
        soc.settimeout(TIMEOUT_SEC)
        return (soc, )

    @staticmethod
    def _main_loop(soc):
        try:
            data, client = soc.recvfrom(self.chunk_size)
            soc.sendto(data, client)
            print(f"Echoed {data} back to {client}")
        except socket.timeout:
            print("Timed out while waiting for data")

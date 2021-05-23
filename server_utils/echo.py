from .abstract import BaseServer
import socket

TIMEOUT_SEC = 1

class EchoServer(BaseServer):
    def __init__(self, address, chunk_size=1024):
        self.address = address
        self.chunk_size = chunk_size

    def _thread_local(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind(self.address)
        soc.settimeout(TIMEOUT_SEC)
        return (soc, )

    def _main_loop(self, soc):
        try:
            data, client = soc.recvfrom(self.chunk_size)
            soc.sendto(data, client)
            print(f"Echoed {data} back to {client}")
        except socket.timeout:
            ...

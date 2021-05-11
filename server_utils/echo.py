from .abstract import BaseServer
import socket

class EchoServer(BaseServer):
    def __init__(self, address, chunk_size=1024):
        self.address = address
        self.chunk_size = chunk_size

    def _thread_local(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind(self.address)
        return (soc, )

    def _main_loop(self, soc):
        data, client = soc.recvfrom(self.chunk_size)
        soc.sendto(data, client)
        print(f"Echoed {data} back to {client}")

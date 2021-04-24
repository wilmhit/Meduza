# check client/audio.py and build compatible code
pass
import socket
from threading import Thread
from voip_server import Server


UDP_IP = "127.0.0.1"
UDP_PORT = 50001

if __name__ == "__main__":
    server = Server(UDP_IP, UDP_PORT)
    server.run()
    #rec_thr = Thread(target=Server.listen)
    #rec_thr.start()

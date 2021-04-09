# check client/audio.py and build compatible code
pass
import socket
from threading import Thread
from voip_server import voip_server

UDP_IP = "127.0.0.1"
UDP_PORT = 50001

if __name__ == "__main__":
    Server = voip_server(UDP_IP, UDP_PORT)
    
    rec_thr = Thread(target=Server.listen)
    rec_thr.start()

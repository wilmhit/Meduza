import socket
from threading import Thread
from client import client

class voip_server:

    def __init__(self, IP_address, IP_port):
        self.IP_address = IP_address
        self.IP_port = IP_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))
        self.channels = [0,1,2,3,4,5,6,7,8,9] #dostępne kanały (kanał 0 - ogólny)
        self.active_cli = 0
        self.next_port = 50100

    def create_client_thread(self):
        cli = client(self.IP_address, self.next_port)
        self.next_port += 1
        client_thr = Thread(target=cli)
        client_thr.start()

    def listen(self):
        print("listen method - ON\n")
        while True:
            data = self.sock.recvfrom(32) # buffer size is 1024 bytes 0 - data, 1 IP [0] / PORT [1] 
            print("received message: %s" % data[0])
            
            
            #MESSAGE = b"PONG"
            #self.sock.sendto(MESSAGE, (data[1][0], data[1][1]))



    


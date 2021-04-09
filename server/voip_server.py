import socket

class voip_server:
    def __init__(self, IP_address, IP_port):
        self.IP_address = IP_address
        self.IP_port = IP_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))

    def listen(self):
        print("listen method - ON\n")
        while True:
            data = self.sock.recvfrom(1024) # buffer size is 1024 bytes 0 - data, 1 IP [0] / PORT [1] 
            print("received message: %s" % data[0])
            MESSAGE = b"PONG"
            self.sock.sendto(MESSAGE, (data[1][0], data[1][1]))
            

    


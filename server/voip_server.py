import socket
from random import randint
from threading import Thread
from client import client


PORT_MIN = 50100
PORT_MAX = PORT_MIN + 500

class ClientManager:

    def __init__(self, IP_address, IP_port, acepted_cb):
        self.IP_address = IP_address
        self.IP_port = IP_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))
        self.acepted_cb = acepted_cb
        
        self.active_cli = 0
        self.next_port = MIN_PORT

    def create_client_thread(self, data):
        #cli = client(self.IP_address, self.next_port) #bindowanie nowego portu dla klienta
        #client_thr = Thread(target=cli.listen) #utworzenie wątku dla klienta na danym porcie
        #client_thr.start() #uruchomienie wątku klienta
        #msg = "SOK" + str(self.next_port)
        self.sock.sendto(bytes('ACC' + , 'utf-8'), data[1]) #przesłanie informacji do klienta o zajmowanym przez niego porcie komunikacyjnym
        print("New client", self.IP_address, "-", self.next_port)
        self.acepted_cb(data[1][0], data[1][1])

    def listen(self):
        print("listen method - ON\n")
        while True:
            data = self.sock.recvfrom(32) #buffer size is 1024 bytes 0 - data, 1 IP [0] / PORT [1] 
            print("received message: %s" % data[0])
            if(str(data[0][0:3], "UTF-8") == "CON"): #żądanie rozpoczącia połączenia
                self.create_client_thread(data)
            else:
                print("Wrong signal from new host  :(")
            
            #MESSAGE = b"PONG"
            #self.sock.sendto(b"hejka", (data[1][0], data[1][1]))




class Server:
    def __init__(self, ip_address, ip_port, channel_0_pass):
        def acepted_cb(client_address, client_port):
            print("Client connected! :)")

        self.main_ip_port = ip_port
        self.main_ip_address = ip_address

        self.channels = {
            0:{
                "port":MIN_PORT,
                "password":channel_0_pass,
                "connected_users":[]   
            }
        }
        for num in range(1,10):
            self.create_channel(num)

        self.client_manager = ClientManager(self.main_ip_address, self.main_ip_port, acepted_cb)

    def create_channel(self, channel_num):
        if channel_num not in self.channels:
            self.channels[channel_num] = {
                "port":self.get_port_num(),
                "password":None,
                "connected_users":[]
            }

    def get_port_num(self):
        port = randint(PORT_MIN, PORT_MAX)
        while self.used(port)
            port = randint(PORT_MIN, PORT_MAX)
        
        return port

    def used(self, port):
        if port == self.main_ip_port:
            return True

        for channel in self.channels:
            if channel.port == port:
                return True
        
        return False


    def run(self):
        
    


from threading import Thread
import time
import socket

class SingleChannel(Thread):
    def __init__(self, number_of_channel, IP_address, IP_port):
        Thread.__init__(self)
        self.number_of_channel = number_of_channel
        self.IP_address = IP_address
        self.IP_port = IP_port
        self.set_up_sock()

        self._running = False

    def set_up_sock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))

    def run(self):
        print("runing thread number: ", self.number_of_channel)

        while self._running:
            print("i'm a thread! :) nubmer: ", self.number_of_channel)
            # TO DO -> nasłuchiwanie na sokocie oraz obsługa / przekazywanie do pozostałych
            time.sleep(1)
        
        print("ups - I'm a dead thread")

    def setUp_start_stop_value(self, empty):
        if empty:
            self._running = True
        else:
            self._running = False

        print("running: ", self._running)


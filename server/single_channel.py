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

    def set_up_sock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))

    def run(self):
        print("runing thread number: ", self.number_of_channel)

        while True:
            print("i'm a thread! :) nubmer: ", self.number_of_channel)
            time.sleep(1.5)


    def if_empty(self):
        pass

    def listen_loop(self):
        pass

    def start_thread(self):
        pass

    def stop_thread(self):
        pass


from threading import Thread
import time

class Single_channel(Thread):
    def __init__(self, number_of_channel):
        Thread.__init__(self)
        self.number_of_channel = number_of_channel
        self.run()

    def run(self):
        print("run threading nr.: ", self.number_of_channel)


    def if_empty(self):
        pass

    def listen_loop(self):
        pass

    def start_thread(self):
        pass

    def stop_thread(self):
        pass


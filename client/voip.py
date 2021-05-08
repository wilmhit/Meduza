import time

class VoipClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
    
    def loop_while(self, variable_set):
        while (variable_set["break_condition"]):
            print("looping")
            time.sleep(0.5)
        print("loop was broken")

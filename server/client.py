import socket


class client:
    def __init__(self, IP_address, IP_port):
        self.IP_address = IP_address
        self.IP_port = IP_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IP_address, self.IP_port))

    def png_signal(self, data): #obsługa sygnału png
        pass

    def con_signal(self, data): #obsługa sygnału con
        pass

    def xxx_signal(self, data): #obsługa sygnału xxx
        pass

    def pas_signal(self, data): #obsługa sygnału pas
        pass

    def signal_read(self, data): #obśługa interpretacji sygnału pakietu
        signal = str(data[0][0:3], "UTF-8") #wyciągnięcie indentyfikatora sygnału (3 pierwsze symbole)
        print(signal)
        if signal == "PNG":
            self.png_signal(data)
        elif signal == "CON":
            self.con_signal(data)
        elif signal == "XXX":
            self.xxx_signal(data)
        elif signal == "PAS":
            self.pas_signal(data)
        else:
            print("signal error")

    def listen(self): #funkcja nasłuchiwania na porcie klienta
        print("Client listen method - ON\n")
        while True:
            data = self.sock.recvfrom(32) #wielkość bufora - 32 bytes [0] - data, [1] IP [0] / PORT [1] 
            print("received message: %s" % data[0])
            self.signal_read(data)    
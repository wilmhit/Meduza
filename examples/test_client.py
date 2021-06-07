import socket
import sys
from threading import Thread
from time import sleep
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
SERVER_ADDRESS = ('127.0.0.1', 10000)

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(('127.0.0.1', 9999))


def receive_thread():
    while True:
        data, addr = soc.recvfrom(CHUNK)
        print(addr, " sends message: ", data)


def send_thread():
    while True:
        sleep(1)
        soc.sendto(b'Hello World', SERVER_ADDRESS)


def main():
    print('Staring Threads...')
    listner = Thread(target=receive_thread)
    sender = Thread(target=send_thread)
    listner.start()
    sender.start()
    print('Threads running...')
    listner.join()
    sender.join()
    print('Shutting down...')


if __name__ == '__main__':
    main()

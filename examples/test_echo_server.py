import socket

CHUNK = 4096
SERVER_ADDRESS = ('127.0.0.1', 10000)

if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(SERVER_ADDRESS)

    print('Server starting...')
    while True:
        data, addr = soc.recvfrom(CHUNK)
        print("Echoed ", data, ' back to ', addr)
        soc.sendto(data, addr)

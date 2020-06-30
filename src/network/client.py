import sys
import socket
import threading
import config


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((socket.gethostname(), PORT))
#
# def send_msg():
#     msg = input('msg: ')
#     client.send((bytes(msg, 'utf-8')))


class Peer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.SERVER_HOST, config.SERVER_PORT))

        self.address = self.socket.getsockname()


    def send(self, data):
        self.socket.send(bytes(data, 'utf-8'))
# py src/network/server.py

if __name__ == '__main__':
    peer = Peer()
    try:
        while 1:
            data = input('data: ')
            if data == '':
                raise KeyboardInterrupt
            peer.send(data)
    except KeyboardInterrupt:
        peer.socket.close()
        sys.exit()

import threading
import socket
import sys
from typing import Union
import config


# while 1:
#     client, address = sock.accept()
#     print(f'connected to {address}')
#     msg = client.recv(1024)
#     print(msg.decode())

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((config.SERVER_HOST, config.SERVER_PORT))
        self.socket.listen(5)

        self.address = self.socket.getsockname()
        print(f'running on {self.address}')
        print(self.socket.getsockname())

    def run(self):
        while 1:
            peer, address = self.socket.accept()
            print(f'Peer connected: {address}')
            thread = threading.Thread(target=self.__listen_to_peer, args=(peer, address))
            thread.daemon = True
            thread.start()

    def __listen_to_peer(self, peer: socket.socket, address: int):
        while 1:
            try:
                msg = peer.recv(1024)
                print(msg.decode())
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()


class PeerTracker:
    peers = []


if __name__ == '__main__':
    server = Server()
    server.run()
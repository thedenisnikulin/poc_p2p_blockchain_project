from typing import List
import threading
import socket
import sys
import config


class Server:
    def __init__(self, host, port):
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind host and port to server and run it
        self.socket.bind((host, port))
        self.socket.listen(5)

        # address in this format: ('127.0.0.1', 1234)
        self.address = self.socket.getsockname()
        print(f'running on {self.address}')

    def run(self):
        """
        Connect peer to the server, run thread for
        listening to peers to receive some data
        """
        while 1:
            peer, address = self.socket.accept()
            print(f'Peer connected: {address}')
            thread = threading.Thread(target=self.__listen_to_peer, args=(peer, address))
            thread.daemon = True
            thread.start()

    def __listen_to_peer(self, peer: socket.socket, address: int):
        """
        Receive peers' messages
        :param peer: peer that comes from socket.accept()
        :param address: address that comes from socket.accept()
        """
        while 1:
            try:
                msg = peer.recv(1024)
                print(msg.decode())
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    server = Server(config.SERVER_HOST, config.SERVER_PORT)
    server.run()

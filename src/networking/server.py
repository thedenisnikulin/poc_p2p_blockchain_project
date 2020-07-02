import sys
import socket
import threading
import pickle
from typing import List
# local
import config
from peer import Peer


class Server(Peer):
    def __init__(self, addr, port):
        super().__init__()
        print('Role: Server')
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        # bind host and port to server and run it
        self.socket.bind((addr, port))
        self.socket.listen(5)

        # address in this format: ('127.0.0.1', 1234)
        self.address = self.socket.getsockname()
        self.peers.add(self.address)
        print(f'running on {self.address}')

    def run(self):
        """
        Connect peer to the server, run thread for
        listening to peers to receive some data
        """
        while 1:
            peer, address = self.socket.accept()
            self.peers.add(address)
            # send list of peers to every peer
            print(f'Peer connected: {address}')
            thread = threading.Thread(target=self.__listen_to_peer, args=(peer, address))
            thread.daemon = True
            thread.start()

    def __listen_to_peer(self, peer: socket.socket, address: int):
        """
        Receive data from peers
        :param peer: peer that comes from socket.accept()
        :param address: address that comes from socket.accept()
        """
        self.broadcast(self.peers)
        while 1:
            try:
                msg = peer.recv(1024)
                print(msg.decode())
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                print(f'Peer disconnected: {address}')
                break

    def close(self):
        self.socket.close()

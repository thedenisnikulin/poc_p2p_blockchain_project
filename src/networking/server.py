import sys
import socket
import threading
import pickle
from typing import List, Set
# local
import config


class Server():
    def __init__(self, addr, port):
        self.peers: Set = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Role: Server')
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        # bind host and port to server and run it
        self.socket.bind((addr, port))
        self.socket.listen(5)
        self.connections: List[socket.socket] = []

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
            conn, address = self.socket.accept()
            self.connections.append(conn)
            self.peers.add(address)
            # send peers to every client
            self.broadcast(self.peers)
            print(f'Peer connected: {address}')
            thread = threading.Thread(target=self.__listen_to_peer, args=(conn, address))
            thread.daemon = True
            thread.start()

    def __listen_to_peer(self, peer: socket.socket, address: int):
        """
        Receive data from peers
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
            except ConnectionResetError:
                print(f'Peer disconnected: {address}')
                break

    def broadcast(self, data):
        print(f'data to send: {data}')
        d = pickle.dumps(data)
        for conn in self.connections:
            conn.send(d)

    def close(self):
        self.socket.close()

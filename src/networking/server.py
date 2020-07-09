import sys
import socket
import threading
import pickle
from typing import List, Set, Tuple
# local
from client import Client
import config


class Server:
    def __init__(self):
        # connections - clients connected to the server
        self.connections: List[socket.socket] = []
        # peers - addresses of each peer in the network
        self.peers: Set = set()
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow connecting to recently closed addresses
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server's address
        self.address = ()

    def connect(self, address: Tuple[str, int]):
        # address in this format: ('127.0.0.1', 1234)
        self.address = address
        # bind address to server and listen
        self.socket.bind(self.address)
        self.socket.listen(5)
        # write address to server_tracker.txt
        self.set_address(self.address)
        # add server's address to peers
        self.peers.add(self.address)

    def run(self):
        """
        Connect peer to the server, run thread for
        listening to peers to receive some data
        """
        while 1:
            # accept client connection
            conn, address = self.socket.accept()
            # add client to connections list and peers list
            self.connections.append(conn)
            self.peers.add(address)
            # send list of peers to every client
            self.broadcast({'peers': self.peers})
            # listen to peer in parallel
            listening_thread = threading.Thread(target=self.__listen_to_peer, args=(conn, address))
            listening_thread.daemon = True
            listening_thread.start()

    def __listen_to_peer(self, conn: socket.socket, address: int):
        """
        Receive data from peers and broadcast it to every peer in the network
        :param conn: connection that comes from socket.accept() (when client connects)
        :param address: address that comes from socket.accept()
        """
        while 1:
            try:
                msg = conn.recv(config.BUFF_SIZE)
                # send received message to every client
                self.broadcast(msg)
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                # when peer disconnects, remove it from peers
                self.peers.remove(address)
                break

    def broadcast(self, data):
        """
        Send some data to client
        :param data: Data that needs to be sent
        """
        if type(data) is bytes:
            data = pickle.loads(data)
        d = pickle.dumps(data)
        for conn in self.connections:
            conn.send(d)

    def close(self):
        self.socket.close()

    @staticmethod
    def get_address():
        """
        Reads server address from ./networking/server_tracker.txt
        :return: server's address, Tuple[str, int]
        """
        with open('./server_tracker.txt', 'r') as file:
            addr = file.readline().split(' ')
            if len(addr) != 2:
                raise Exception('No address found in server_tracker.txt.')
            return addr[0], int(addr[1])

    @staticmethod
    def set_address(addr: Tuple[str, int]):
        """
        Writes server address to ./networking/server_tracker.txt
        :param addr: address to write, Tuple[str, int]
        """
        with open('./server_tracker.txt', 'w') as file:
            file.write(f'{addr[0]} {addr[1]}')


class SuperPeer:
    """
    A super Peer - server + client. Manages connections.
    """
    def __init__(self):
        self.server = Server()
        self.client = Client()

    def close_connections(self):
        self.client.socket.close()
        self.server.close()


def get_current_ip_address() -> Tuple[str, int]:
    """
    These weird socket manipulations are just to get current address of the current socket
    :return: address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 9865))
    s.listen()
    c.connect((socket.gethostname(), 9865))
    try:
        return c.getsockname()
    finally:
        s.close()
        c.close()
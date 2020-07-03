import sys
import socket
import threading
import pickle
from typing import List, Set, Tuple
# local
import config


class Server:
    def __init__(self):
        # connections - clients connected to the server
        self.connections: List[socket.socket] = []
        # peers - addresses of each peer in the network
        self.peers: Set = set()
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind host and port to server and listen
        # TODO: When server connects, it's okay, but when client try to become server - it gets connected to new port
        self.address = get_address()
        # self.address = Server.get_address()
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.set_address(self.address)

        # address in this format: ('127.0.0.1', 1234)
        # add server's address to peers
        self.peers.add(self.address)
        print('Role: Server')
        print(f'Running on {self.address}')

    def run(self):
        """
        Connect peer to the server, run thread for
        listening to peers to receive some data
        """
        while 1:
            print('run')
            conn, address = self.socket.accept()
            print('got client')
            # add client to connections and peers
            self.connections.append(conn)
            self.peers.add(address)
            # send list of peers to every client
            self.broadcast(self.peers)
            print(f'Peer connected: {address}')
            thread = threading.Thread(target=self.__listen_to_peer, args=(conn, address))
            thread.daemon = True
            thread.start()

    def __listen_to_peer(self, conn: socket.socket, address: int):
        """
        Receive data from peers
        :param conn: connection that comes from socket.accept()
        :param address: address that comes from socket.accept()
        """
        print('listen to peer')
        while 1:
            try:
                msg = conn.recv(config.BUFF_SIZE)
                self.broadcast(msg.decode())
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                print(f'Peer disconnected: {address}')
                break

    def broadcast(self, data):
        """
        Send some data to client
        :param data: Data that needs to be sent
        """
        print(f'data to send: {data}')
        d = pickle.dumps(data)
        for conn in self.connections:
            conn.send(d)

    def close(self):
        self.socket.close()

    @staticmethod
    def get_address():
        with open('./server_tracker', 'r') as file:
            addr = file.read().split(' ')
            return str(addr[0]), int(addr[1])

    @staticmethod
    def set_address(addr: Tuple[str, int]):
        with open('./server_tracker', 'w') as file:
            file.write(f'{addr[0]} {addr[1]}')


def get_address() -> Tuple[str, int]:
    """
    Just to get current address
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

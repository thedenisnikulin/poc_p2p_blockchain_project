import sys
import socket
import pickle
import threading
from typing import Set, Tuple
# local
import config
from blockchain.Blockchain import Blockchain
from blockchain.cli_interface import use_blockchain


class Client:
    def __init__(self):
        # peers - addresses of each peer in the network
        self.peers: Set = set()
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow connecting to recently closed addresses
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address in such format: ("1.1.1.1", 1111)
        self.address = ()
        self.server_address = ()
        # init blockchain
        self.blockchain = Blockchain()

    def connect(self, server_address: Tuple[str, int]):
        print(f'Client is connecting...')
        # connect to server
        self.socket.connect(server_address)
        self.address = self.socket.getsockname()
        self.peers.add(self.address)
        self.server_address = self.socket.getpeername()
        print(f'Role: Client \nAddress: {self.address}')
        print(f'server is on {self.server_address}')

        self.blockchain.generate_genesis_block()
        self.sync_peers()
        self.__listen_to_user_input()

    def __listen_to_user_input(self):
        print('Client is listening to input...')
        """
        Listen to data to send to the server (infinite loop)
        """
        try:
            th = threading.Thread(target=self.__listen_to_server)
            th.daemon = True
            th.start()
            use_blockchain(self.socket,
                           self.blockchain,
                           set([p for p in self.peers if p != self.address and p != self.server_address]))
        # exit
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

    def __listen_to_server(self):
        print('Client is ready to receive')
        while 1:
            try:
                # d - data that client receives
                d = self.socket.recv(4096)
                d = pickle.loads(d)
                print(d)
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                print('Connection reset. Press [ Enter ] to continue.')
                break

    def sync_peers(self):
        """
        Update local peers by ones received from server = synchronize
        """
        print('Syncing peers...')
        d = self.socket.recv(config.BUFF_SIZE)
        d = pickle.loads(d)
        self.peers.update(d)
        print(f'synced{self.peers}')

    def send(self, data_to_send):
        """
        Send data to the server
        """
        self.socket.send(bytes(data_to_send, 'utf-8'))

    def close_connection(self):
        self.socket.close()


class Peer(Client):
    """
    A simple client.
    """

    def __init__(self):
        super().__init__()
        self.blockchain: Blockchain

    def reset_connection(self):
        """
        Reset peer connection - reinitialize.
        """
        data = (self.peers,)
        super().__init__()
        self.peers = data[0]

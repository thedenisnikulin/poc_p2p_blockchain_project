import sys
import socket
import pickle
import threading
# local
import config
from typing import Set, Tuple


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

    def connect(self, server_address: Tuple[str, int]):
        print(f'connect')
        # connect to server
        self.socket.connect(server_address)
        self.address = self.socket.getsockname()
        self.peers.add(self.address)
        print(f'Role: Client \nAddress: {self.address}')
        # # FIXME: how it works lol
        # sync_t = threading.Thread(target=self.sync_peers)
        # sync_t.daemon = True
        # sync_t.start()
        # listen_t = threading.Thread(target=self.__listen_to_input())
        # listen_t.daemon = True
        # listen_t.start()

    def __listen_to_input(self):
        print('listen to input')
        """
        Listen to data to send to the server (infinite loop)
        """
        th = threading.Thread(target=self.receive)
        th.daemon = True
        th.start()
        try:
            while 1:
                data = input('data: ')
                if data == '':
                    break
                self.send(data)
        # exit from the loop
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

    def receive(self):
        print('rec')
        d = self.socket.recv(4096)
        print(pickle.loads(d))

    def sync_peers(self):
        """
        Update local peers by ones received from server = synchronize
        """
        print('sync')
        d = self.socket.recv(config.BUFF_SIZE)
        d = pickle.loads(d)
        self.peers.update(d)
        print(self.peers)
        print('end sync')

    def send(self, data_to_send):
        """
        Send data to the current server
        :param data_to_send: some data to send
        """
        self.socket.send(bytes(data_to_send, 'utf-8'))

    @property
    def __str__(self):
        return ('-' * 4 + 'peers' + 4 * '-' + '\n'
                + ''.join([str(p) + '\n' for p in self.peers])
                + 13 * '-' + '\n')
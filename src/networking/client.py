import sys
import socket
import pickle
import threading
from typing import Set, Tuple
# local
import config

actions = 6*"-" + "Actions" + "-"*6 + "\n" + \
            "[0] Get chain\n" + \
            "[1] New transaction\n" + \
            "[2] Mine block\n" + \
          6*"-" + "-------" + "-"*6 + "\n"


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

        self.sync_peers()
        self.__listen_to_user_input()

    def __listen_to_user_input(self):
        print('listen to input')
        """
        Listen to data to send to the server (infinite loop)
        """
        try:
            th = threading.Thread(target=self.__listen_to_server)
            th.daemon = True
            th.start()
            while 1:
                data = input('data: ')
                # if data == '':
                #     break
                self.send(data)
        # exit from the loop
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()
        except ConnectionResetError:
            print('WIN ERROR OCCURED')

    def __listen_to_server(self):
        print('receive')
        while 1:
            try:
                d = self.socket.recv(4096)
                d = pickle.loads(d)
                print(d)
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                #
                print('Connection reset. Press [ Enter ] to continue.')
                break

    def sync_peers(self):
        """
        Update local peers by ones received from server = synchronize
        """
        print('sync')
        d = self.socket.recv(config.BUFF_SIZE)
        d = pickle.loads(d)
        self.peers.update(d)
        print(f'synced{self.peers}')

    def send(self, data_to_send):
        """
        Send data to the server
        """
        self.socket.send(bytes(data_to_send, 'utf-8'))

    @property
    def __str__(self):
        return ('-' * 4 + 'peers' + 4 * '-' + '\n'
                + ''.join([str(p) + '\n' for p in self.peers])
                + 13 * '-' + '\n')
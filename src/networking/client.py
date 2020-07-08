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
        self.address: Tuple[str, int] = ()
        self.server_address = ()
        # initialize blockchain
        self.blockchain = Blockchain()

    def connect(self, server_address: Tuple[str, int]):
        print(f'Client is connecting...')
        # connect to server
        self.socket.connect(server_address)
        self.address = self.socket.getsockname()
        self.server_address = self.socket.getpeername()
        self.peers.add(self.address)
        print(f'Role: Client \nAddress: {self.address}')

        self.blockchain.generate_genesis_block()
        th = threading.Thread(target=self.__listen_to_server)
        th.daemon = True
        th.start()
        self.__listen_to_user_input()

    def __listen_to_user_input(self):
        print('clis_i')
        """
        Listen to data to send to the server (infinite loop)
        """
        try:
            while 1:
                # FIXME: when new peers get received, they are passed to use_blockchain only after an iteration
                use_blockchain(
                    self.blockchain,
                    self.address,
                    set([p for p in self.peers
                        if p != self.address and p != self.server_address])
                )
                self.send()
        # exit from the loop
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

    def __listen_to_server(self):
        print('clis_s')
        while 1:
            try:
                # receive data
                data = self.socket.recv(config.BUFF_SIZE)
                data = pickle.loads(data)
                print(data)
                # update local peers
                self.peers = data['peers']

                # if there's not only peers that came from server:
                if len(data) > 1:
                    new_chain = data['blockchain']['chain']
                    new_pending_transactions = data['blockchain']['pending_transactions']
                    # if new chain is valid
                    if self.blockchain.is_valid(new_chain):
                        # replace local chain and pending transactions
                        self.blockchain.replace_chain(new_chain)
                        self.blockchain.pending_transactions = new_pending_transactions
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except ConnectionResetError:
                print('Connection reset. Press [ Enter ] to continue.')
                break

    def send(self):
        """
        Send data to the server
        """
        # data is sent in such protocol: peers & blockchain
        data = {
            'peers': self.peers,
            'blockchain': {
                'chain': self.blockchain.chain,
                'pending_transactions': self.blockchain.pending_transactions
            }
        }
        data = pickle.dumps(data)
        self.socket.send(data) # self.socket.send(bytes(data_to_send, 'utf-8'))

    def close_connection(self):
        self.socket.close()


class Peer(Client):
    """
    A simple client.
    """

    def __init__(self):
        super().__init__()

    def reset_connection(self):
        """
        Reset peer connection - reinitialize.
        """
        # save data from client
        peers = self.peers
        blockchain = self.blockchain
        # reset client
        super().__init__()
        # load data to client
        self.peers = peers
        self.blockchain = blockchain

import sys
import socket
import pickle
import threading
from typing import Set, Tuple
# local
from networking import config
from blockchain.Blockchain import Blockchain
from blockchain.cli_interface import use_blockchain, clearconsole


class Client:
    def __init__(self):
        # peers - addresses of each peer in the network
        self.peers = set()
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow connecting to recently closed addresses
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # addresses in such format: ("1.1.1.1", 1111)
        self.address: Tuple[str, int] = ()
        self.server_address: Tuple[str, int] = ()
        # initialize blockchain
        self.blockchain = Blockchain()

    def connect(self, server_address: Tuple[str, int]):
        """
        Connect to server.
        :param server_address: address to connect to
        """
        # connect to server
        self.socket.connect(server_address)
        # set addresses
        self.address = self.socket.getsockname()
        self.server_address = self.socket.getpeername()
        # add current client to local peers
        self.peers.add(self.address)

        # generate genesis block
        self.blockchain.generate_genesis_block()
        # run listening to server in parallel
        th = threading.Thread(target=self.__listen_to_server)
        th.daemon = True
        th.start()
        # execute main logic - listening to user that interacts with blockchain
        self.__listen_to_user_input()

    def __listen_to_user_input(self):
        """
        Listen to data to send to the server (infinite loop)
        """
        try:
            while 1:
                use_blockchain(
                    self.blockchain,
                    self.address,
                    set([p for p in self.peers
                        if p != self.address and p != self.server_address])
                )
                # send all the new stuff that we made with our blockchain instance
                self.send()
        # exit from the loop
        except KeyboardInterrupt:
            print("it was raised") # TODO fix program is not terminated
            self.close()
            sys.exit()

    def __listen_to_server(self):
        while 1:
            # receive data - peers list and blockchain instance
            try:
                data = self.socket.recv(config.BUFF_SIZE)
            except ConnectionResetError:
                # Happens when server disconnects. Hit Enter and it will break the loop
                clearconsole()
                print('Connection reset. Press [ Enter ] to reconnect.')
                break
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            
            try:
                data = pickle.loads(data)
            except EOFError:
                # Happens when server disconnects. Hit Enter and it will break the loop
                clearconsole()
                print('Connection reset. Press [ Enter ] to reconnect.')
                break
            # update local peers
            self.peers = data['peers']

            # if there's also a blockchain that came from server:
            if len(data) > 1:
                new_chain = data['blockchain']['chain']
                new_pending_transactions = data['blockchain']['pending_transactions']
                # and if new chain is valid
                if self.blockchain.is_valid(new_chain):
                    # replace local chain and pending transactions with new ones
                    self.blockchain.replace_chain(new_chain)
                    self.blockchain.pending_transactions = new_pending_transactions


    def send(self):
        """
        Send data to the server
        """
        # data to send:
        # peers - list of local peers
        # blockchain - the chain itself and pending transactions
        data = {
            'peers': self.peers,
            'blockchain': {
                'chain': self.blockchain.chain,
                'pending_transactions': self.blockchain.pending_transactions
            }
        }
        data = pickle.dumps(data)
        self.socket.send(data)

    def close(self):
        self.socket.close()


class Peer(Client):
    """
    A classic peer - only client.
    """
    def __init__(self):
        super().__init__()

    def reset_connection(self):
        """
        Reset peer connection - reinitialize it.
        """
        # save data
        addr = self.address
        peers = self.peers
        blockchain = self.blockchain
        # reset client
        super().__init__()
        # load data
        self.socket.bind(addr)
        self.peers = peers
        self.blockchain.chain = blockchain.chain
        self.blockchain.pending_transactions = blockchain.pending_transactions
        # return address to use it when constructing SuperPeer later. See main.py
        # Blockchain will be used in SuperPeer as well.
        # We don't return peers 'cos SuperPeer will connect peers by itself.
        return addr, blockchain

from socket import socket
from typing import Set, Tuple
import socket
import pickle


class Peer:
    """
       Base peer class
    """

    def __init__(self):
        self.address: Tuple = ()
        self.peers: Set = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast(self, data):
        print(f'data to send: {data}')
        d = pickle.dumps(data)
        peers = self.peers
        peers.remove(self.address)
        for peer in peers:
            print(f'prepare {peer}, {type(peer)}')
            while 1:
                try:
                    self.socket.sendto(d, peer)
                except OSError as e:
                    print(e)
                break
            print('done!')

    def update_peers(self, peers: Set):
        self.peers.update(peers)

    @property
    def __str__(self):
        return ('-' * 4 + 'peers' + 4 * '-' + '\n'
                + ''.join([str(p) + '\n' for p in self.peers])
                + 13 * '-' + '\n')

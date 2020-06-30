import sys
import socket
import threading
import config
from server import Server


class Peer:
    def __init__(self):
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the current server
        self.socket.connect((config.SERVER_HOST, config.SERVER_PORT))
        # allow connect to recently closed socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address in this format: ('127.0.0.1', 1234)
        self.address = self.socket.getsockname()

    def send(self, data_to_send):
        """
        Send data to the current server
        :param data_to_send: some data to send
        """
        self.socket.send(bytes(data_to_send, 'utf-8'))

    def start_execution(self):
        """
        Ask for data in infinite loop to send to the server
        :return:
        """
        try:
            while 1:
                data = input('data: ')
                if data == '':
                    raise KeyboardInterrupt
                self.send(data)
        # exit from the loop
        except KeyboardInterrupt:
            self.socket.close()
            sys.exit()

# py src/network/server.py

class PeerTracker:
    """
    Track peers connected to the server
    """
    peers = []


if __name__ == '__main__':
    print('-'*4 + 'peers' + 4*'-')
    [print(p) for p in PeerTracker.peers]
    print(13*'-')
    # if there're no peers in the network - create a server
    if len(PeerTracker.peers) == 0:
        print('I am a server!')
        server = Server(config.SERVER_HOST, config.SERVER_PORT)
        PeerTracker.peers.append(server.address)
        try:
            server.run()
        except KeyboardInterrupt:
            PeerTracker.peers.remove(server.address)
            server.close()
    # else - create a peer
    else:
        print('I am a peer!')
        peer = Peer()
        PeerTracker.peers.append(peer.address)
        try:
            peer.start_execution()
        # when current server can't be reached (disabled) it picks
        # one peer and makes a server out of that peer
        except ConnectionResetError:
            print(f'err occurred\npeers: {[i for i in PeerTracker.peers]}')
            server = Server(PeerTracker.peers[0][0], PeerTracker.peers[0][1])
            server.run()

import socket
import random
import sys
import threading
from typing import Tuple
# local
from server import Server
from client import Client
import config


class Peer(Client):
    def __init__(self):
        super().__init__()


class SuperPeer:
    def __init__(self):
        self.server = Server()
        self.client = Client()


if __name__ == '__main__':
    while 1:
        try:
            peer = Peer()
            peer.connect(Server.get_address())
        except ConnectionResetError:
            # if current server can't be reached (connection reset)
            # pick one client and make a server out of it
            pass
        except WindowsError:
            # no server on provided port
            pass

        try:
            super_peer = SuperPeer()
            c_t = threading.Thread(target=super_peer.client.connect, args=super_peer.server.address)
            c_t.daemon = True
            c_t.start()
            s_t = threading.Thread(target=super_peer.server.run)
            s_t.daemon = True
            s_t.start()
        except KeyboardInterrupt:
            sys.exit()
        except OSError:
            pass
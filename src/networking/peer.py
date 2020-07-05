import socket
import random
import sys
import threading
from typing import Tuple
# local
from server import Server, get_current_ip_address
from client import Client
import config


class Peer(Client):
    def __init__(self):
        super().__init__()


class SuperPeer:
    def __init__(self, address: Tuple[str, int]):
        self.server = Server(address)
        self.client = Client()


if __name__ == '__main__':
    while 1:
        try:
            peer = Peer()
            peer.connect(Server.get_address())
        except ConnectionResetError:
            # Server disconnected
            pass
        except WindowsError:
            # No server
            print('we')
            pass

        try:
            super_peer = SuperPeer(Server.get_address())
        except OSError:
            continue
        except KeyboardInterrupt:
            sys.exit()
        else:
            client_worker = threading.Thread(target=super_peer.client.connect, args=(super_peer.server.address,))
            client_worker.daemon = True
            client_worker.start()
            super_peer.server.run()

        # try:
        #     super_peer = SuperPeer()
        #     c_t = threading.Thread(target=super_peer.client.connect, args=(super_peer.server.address, ))
        #     c_t.daemon = True
        #     c_t.start()
        #     super_peer.server.run()
        # except KeyboardInterrupt:
        #     sys.exit()
        # except OSError:
        #     # Server already provided on that address
        #     pass
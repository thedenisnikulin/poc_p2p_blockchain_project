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
    """
    A simple client.
    """
    def __init__(self):
        super().__init__()

    def close_connection(self):
        self.socket.close()


class SuperPeer:
    """
    Server + client. Manages connections.
    """
    def __init__(self):
        self.server = Server()
        self.client = Client()

    def close_connections(self):
        self.client.socket.close()
        self.server.close()


def main():
    # initialize two states - Peer and SuperPeer
    peer = Peer()
    super_peer = SuperPeer()
    # start execution loop
    while 1:
        # Become Peer firstly
        try:
            try:
                # Try to connect to the address from server_tracker.txt
                peer.connect(Server.get_address())
            except WindowsError as e:
                # If it failed, pass the error and go iterate through peers
                print('LOOOOOOL')
                print(e)
                pass
            # try to connect to every local peer that current Peer has in its peers list
            # if no local peers, then do nothing
            for p in peer.peers:
                print(f'connecting to {p}')
                try:
                    peer.connect(p)
                except WindowsError as e:
                    print(e)
                    print('not a server')
                    continue
                else:
                    print('found a server!')
        except WindowsError as exc:
            if exc.errno == 10061:
                # No server found on current address
                print('first')
                print(exc)
                pass
            elif exc.errno == 10054:
                # Found server is disconnected
                print('second')
                print(exc)
                continue

        peer.close_connection()
        print(14*'-' + 'SWITCH' + '-'*14)
        # If all Peer stuff done and it has nothing to do with it anymore,
        # become a SuperPeer

        # Become a SuperPeer
        try:
            try:
                # if it was simply Peer before, try to create SuperPeer based on Peer's port
                # Because we want SuperPeer to stay on the same address that Peer was on
                super_peer.server.connect(peer.address)
            except TypeError:
                # If there's no Peer address (so it wasn't Peer before, it is originally a SuperPeer),
                # then get current ip address and connect to it
                print('typeerror')
                super_peer.server.connect(get_current_ip_address())
        except OSError:
            # Server is already provided
            super_peer.close_connections()
            print('oserr server')
            continue
        except KeyboardInterrupt:
            # Hit break (ctrl + C)
            super_peer.close_connections()
            sys.exit()
        else:
            # Start client in parallel
            client_worker = threading.Thread(target=super_peer.client.connect, args=(super_peer.server.address,))
            client_worker.daemon = True
            client_worker.start()
            # Start server
            super_peer.server.run()

if __name__ == '__main__':
    main()
    # while 1:
    #     try:
    #         peer = Peer()
    #         peer.connect(Server.get_address())
    #     except ConnectionResetError:
    #         # Server disconnected
    #         pass
    #     except WindowsError:
    #         # No server
    #         print('we')
    #         pass
    #
    #     try:
    #         super_peer = SuperPeer(Server.get_address())
    #     except OSError:
    #         continue
    #     except KeyboardInterrupt:
    #         sys.exit()
    #     else:
    #         client_worker = threading.Thread(target=super_peer.client.connect, args=(super_peer.server.address,))
    #         client_worker.daemon = True
    #         client_worker.start()
    #         super_peer.server.run()
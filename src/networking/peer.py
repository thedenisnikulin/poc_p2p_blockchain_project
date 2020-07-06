import sys
import threading
# local
from server import Server, get_current_ip_address
from client import Client


class Peer(Client):
    """
    A simple client.
    """
    def __init__(self):
        super().__init__()

    def close_connection(self):
        self.socket.close()

    def reset_connection(self):
        """
        Resets peer connection.
        """
        super().__init__()


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
            # Try to connect to the address from server_tracker.txt
            peer.connect(Server.get_address())
        except WindowsError as exc:
            if exc.errno == 10061:
                # No server found on current address
                print('first')
                print(exc)
                # we can ignore it (pass) because it happens when there's no SuperPeer at all
                pass
            elif exc.errno == 10054:
                # Found server is disconnected
                print('second')
                print(exc)
                # we have have to reset connection and connect again,
                # because SuperPeer is now on another address
                peer.reset_connection()
                continue

        # If all Peer stuff done and it has nothing to do with it anymore, become a SuperPeer
        print(14*'-' + 'SWITCH' + '-'*14)

        # Become a SuperPeer
        try:
            try:
                # if it was simply Peer before, try to create SuperPeer based on Peer's port
                # Because we want SuperPeer to stay on the same address that Peer was on
                super_peer.server.connect(peer.address)
            except TypeError:
                # If there's no Peer address - TypeError happens
                # (so it wasn't Peer before, it is originally a SuperPeer),
                # then get current ip address and connect to it
                super_peer.server.connect(get_current_ip_address())
        except OSError:
            # Server is already provided
            super_peer.close_connections()
            print('oserr server')
            continue
        except (KeyboardInterrupt, SystemExit):
            # Hit break (ctrl + C) OR exit (stop terminal)
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
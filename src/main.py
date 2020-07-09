import sys
import threading
# local
from blockchain.Blockchain import Blockchain
from server import SuperPeer, Server, get_current_ip_address
from client import Peer


def main():
    # initialize two states - Peer and SuperPeer
    peer = Peer()
    super_peer = SuperPeer()
    # when peer resets connection, we need it to save its data (address and blockchain) as it was before reset,
    # so we store its data in these variables. Initially, address is None and blockchain is an empty Blockchain object,
    # but when connection resets, they get assigned
    address = None
    blockchain: Blockchain = Blockchain()
    # start execution loop
    while 1:
        # Become Peer firstly
        try:
            # Try to connect to the address from server_tracker.txt
            peer.connect(Server.get_address())
        except WindowsError as exc:
            if exc.errno == 10061:
                # 10061 - No server found on the address

                # we can ignore it (pass) because it happens when there's no SuperPeer at all,
                # so we need to create one by passing control to SuperPeer state
                pass
            elif exc.errno == 10054:
                # 10054 - Found server is disconnected

                # we have have to reset Peer's connection and connect again,
                # because SuperPeer is now on another address
                address, blockchain = peer.reset_connection()
                continue


        # If all Peer stuff done and it has nothing to do with it anymore, become a SuperPeer


        # Become a SuperPeer
        try:
            super_peer.server.connect(get_current_ip_address())
        except OSError:
            # Server is already provided
            super_peer.close_connections()
            continue
        except (KeyboardInterrupt, SystemExit):
            # Hit break (ctrl + C) OR exit (stop terminal)
            super_peer.close_connections()
            sys.exit()
        else:
            # if we don't do that, SuperPeer's client starts on a new address with empty Blockchain instance,
            # which is not what we need.
            if address is not None:
                super_peer.client.socket.bind(address)
                super_peer.client.blockchain.chain = blockchain.chain
                super_peer.client.blockchain.pending_transactions = blockchain.pending_transactions
            # Start client in parallel
            client_worker = threading.Thread(target=super_peer.client.connect, args=(super_peer.server.address,))
            client_worker.daemon = True
            client_worker.start()
            # Start server
            super_peer.server.run()


if __name__ == '__main__':
    main()

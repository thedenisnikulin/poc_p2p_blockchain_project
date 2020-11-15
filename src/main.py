import sys
import threading
# local
from blockchain.Blockchain import Blockchain
from networking.server import SuperPeer, Server
from networking.client import Peer


def main():
	# initialize two states - Peer and SuperPeer
	peer = Peer()
	super_peer = SuperPeer()
	# when peer resets connection, we need it to save its data (address and blockchain) as it was before the reset,
	# so we store its data in these variables. Initially, address is None and blockchain is an empty Blockchain object,
	# but when connection resets, they get assigned
	address = None
	blockchain = Blockchain()
	# start execution loop
	while 1:
		# Become a Peer firstly
		try:
			# Try to connect to address from server_tracker.txt
			peer.connect_and_run(Server.read_address("./server_tracker.txt"))
		except OSError as exc:
			if exc.errno == 111:
				# 111 - Connection refused.
				# It means there's no server found on provided port.

				# We can ignore this error (pass) because it happens when there's no SuperPeer at all,
				# so we just need to proceed in order to become one.
				pass
			elif exc.errno == 32:
				# 32 - Broken pipe.
				# It means found server is disconnected, i.e. server socket is closed.

				# We have to reinitialize and try to connect again,
				# because SuperPeer is now on another address
				(address, blockchain) = peer.reinit()
				continue
			elif exc.errno == 2:
				# 2 - FileNotFoundError (server_tracker.txt)

				# We can pass because SuperPeer will create the file.
				pass

		# Become a SuperPeer
		try:
			# Specify zero port to make socket be bound on any available port
			super_peer.server.listen(('', 0))
		except OSError:
			# Error: server is already provided
			super_peer.close_connections()
			continue
		else:
			# "else" block executes when there were no exceptions raised.
			if address is not None:
				# Happens when the current process previously was a Peer.
				# Bind SuperPeer's client on Peer's address; pass blockchain.
				super_peer.client.socket.bind(address)
				super_peer.client.blockchain.chain = blockchain.chain
				super_peer.client.blockchain.pending_transactions = blockchain.pending_transactions
			# Start client in parallel
			client_worker = threading.Thread(
				target=super_peer.client.connect_and_run, 
				args=(super_peer.server.address,)
			)
			client_worker.daemon = True
			client_worker.start()
			# Start server
			try:
				super_peer.server.run()
			except (KeyboardInterrupt, SystemExit):
				# Hit break (ctrl + c)
				super_peer.close_connections()
				sys.exit()


if __name__ == '__main__':
	main()

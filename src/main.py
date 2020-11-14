import sys
import threading
# local
from blockchain.Blockchain import Blockchain
from networking.server import SuperPeer, Server
from networking.client import Peer

def log(msg):
	print(30*'-' + msg + '-'*30)

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
		# Become Peer firstly
		try:
			# Try to connect to the address from server_tracker.txt
			peer.connect_and_run(Server.read_address("./server_tracker.txt"))
		except OSError as exc:
			if exc.errno == 111:
				log("111 CONN REFUSED")
			#if exc.errno == 10061:
				# 10061 - No server found on the address

				# We can ignore this error (pass) because it happens when there's no SuperPeer at all,
				# so we need to create one by passing control to SuperPeer state.
				# Don't forget to close peer socket
				#peer.close()
				pass
			elif exc.errno == 32: # broken pipe
				log("32 BROKEN PIPE")
			#elif exc.errno == 10054:
				# 10054 - Found server is disconnected 

				# we have have to reset Peer's connection and try to connect again,
				# because SuperPeer is now on another address
				address, blockchain = peer.reset_connection()
				continue
			elif exc.errno == 2:
				# FileNotFoundError (server_tracker.txt)
				pass
		

		# If all Peer stuff done and it has nothing to do with it anymore, become a SuperPeer


		# Become a SuperPeer
		try:
			# Specify zero port to make socket be bound on any available port
			super_peer.server.listen(('', 0))
		except OSError as exc:
			log(f"[super] {exc.errno}: {exc}")
			# Error: server is already provided
			super_peer.close_connections()
			continue
		else:
			# "else" block executes when there were no exceptions raised.
			# If we don't do that, SuperPeer's client starts on a new address with empty blockchain instance,
			# which is not what we want.
			if address is not None:
				# Bind SuperPeer's client on Peer's address; pass blockchain
				super_peer.client.socket.bind(address)
				super_peer.client.blockchain.chain = blockchain.chain
				super_peer.client.blockchain.pending_transactions = blockchain.pending_transactions
			# Start client in parallel
			client_worker = threading.Thread(target=super_peer.client.connect_and_run, args=(super_peer.server.address,))
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

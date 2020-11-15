import sys
import socket
import threading
import pickle
from typing import List, Set, Tuple
# local
from networking.client import Client
from networking import config

class Server:
	def __init__(self):     # TODO make some fields private
		# Connections - clients connected to the server.
		self.connections: List[socket.socket] = []
		# Peers - addresses of each peer in the network.
		self.peers = []
		# Initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP.
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Allow connecting to recently closed addresses.
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Server address.
		self.address = ()

	def listen(self, address: Tuple[str, int]): 
		# Bind address to server and listen.
		self.socket.bind(address)
		self.socket.listen()
		# Set socket address.
		self.address = self.socket.getsockname()
		# Write address to server_tracker.txt.
		self.write_address("./server_tracker.txt", self.address)
		# Add server address to peers.
		self.peers.append(self.address)

	def run(self):
		"""
		Connect peer to the server, run thread for
		listening to peers to receive some data
		"""
		while 1:
			# Accept client connection.
			try:
				(conn, address) = self.socket.accept()
			except KeyboardInterrupt:
				self.close()
				sys.exit()
			# Add client to connections list and peers list.
			self.connections.append(conn)
			self.peers.append(address)
			# Send list of peers to every client.
			self.broadcast({'peers': self.peers})
			# Listen to peer in parallel.
			listening_thread = threading.Thread(target=self.__listen_to_peer, args=(conn, address))
			listening_thread.daemon = True
			listening_thread.start()

	def __listen_to_peer(self, conn: socket.socket, address: int):
		"""
		Receive data from a peer and broadcast it to every peer in the network
		:param conn: connection that comes from socket.accept() (when client connects)
		:param address: address that comes from socket.accept()
		"""
		while 1:
			try:
				msg = conn.recv(config.BUFF_SIZE)
				# Send received message to every client.
				self.broadcast(msg)
			except KeyboardInterrupt:
				self.close()
				sys.exit()
			except (EOFError, ConnectionResetError):
				# EOFError: when pickle runs out of input.
				# ConnectionResetError: when connection to client is lost.
				# When peer disconnects, remove it from peers and connections.
				self.peers.remove(address)
				self.connections.remove(conn)
				# Send updated list of peers.
				self.broadcast({'peers': self.peers})
				break

	def broadcast(self, data):
		"""
		Send some data to client
		:param data: Data that needs to be sent
		"""
		if type(data) is bytes:
			data = pickle.loads(data)
		d = pickle.dumps(data)
		for conn in self.connections:
			conn.send(d)

	def close(self):
		self.socket.close()

	@staticmethod
	def read_address(file_path):
		"""
		Reads server address from specified file
		:param file_path: path to the file with address written to it
		:return: server address
		"""
		with open(file_path, 'r') as file:
			addr = file.readline().split(' ')
			if len(addr) != 2:
				raise Exception(f"Invalid address in {file_path}.")
			return (addr[0], int(addr[1]))

	@staticmethod
	def write_address(file_path: str, addr: Tuple[str, int]):
		"""
		Writes server address to server_tracker.txt
		:param file_path: path to file to write to
		:param addr: address to write
		"""
		with open(file_path, 'w') as file:
			file.write(f'{addr[0]} {addr[1]}')


class SuperPeer:
	"""
	SuperPeer: server + client.
	Manages connections.
	"""
	def __init__(self):
		self.server = Server()
		self.client = Client()

	def close_connections(self):
		self.client.close()
		self.server.close()

import sys
import socket
import threading
import pickle
# local
import config
from server import Server
from peer import Peer


class Client(Peer):
    def __init__(self):
        super().__init__()
        print('Role: Client')
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        # connect to the current server
        self.socket.connect((config.SERVER_ADDR, config.SERVER_PORT))
        # allow connect to recently closed sockets
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address in this format: ('127.0.0.1', 1234)
        self.address = self.socket.getsockname()
        self.peers.add(self.address)

    def receive(self):
        d = None  # data ro receive
        while d is None:
            print(f'receive loop\ni\'m {self.address}')
            d, addr = self.socket.recvfrom(4096)  # 4096 because I saw that on stack overflow, lol
            print(f'from {addr}')
            if d != b'':
                print(d)
                d = pickle.loads(d)
                print(f'{d}, of type {type(d)}')
        return d

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


if __name__ == '__main__':
    while 1:
        try:
            server = Server(config.SERVER_ADDR, config.SERVER_PORT)
            server.run()
        except KeyboardInterrupt:
            server.close()
        except OSError:
            print('Server is already provided. You\'re now a Client.')
            pass

        try:
            client = Client()
            data = client.receive()
            # client.update_peers(data)
            # client.broadcast(client.peers)
            # client.start_execution()
            # when current server can't be reached (disabled) it picks
            # one peer and makes a server out of that peer
        except ConnectionResetError:
            print(f'Connection Reset Error Occured\n{client.__str__}')
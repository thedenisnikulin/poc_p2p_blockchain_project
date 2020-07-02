import sys
import socket
import threading
import pickle
# local
import config
from server import Server
from typing import Set


class Client():
    def __init__(self):
        print('Role: Client')
        self.peers: Set = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # initialize socket - AF_INET means IPv4, SOCK_STREAM means TCP
        # connect to the current server
        self.socket.connect((config.SERVER_ADDR, config.SERVER_PORT))
        # allow connect to recently closed sockets
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address in this format: ('127.0.0.1', 1234)
        self.address = self.socket.getsockname()
        self.peers.add(self.address)

        # update peers received from server
        self.update_peers()

    def update_peers(self):
        d = self.socket.recv(config.BUFF_SIZE)  # 4096 because I saw that on stack overflow, lol
        d = pickle.loads(d)
        self.peers.update(d)
        print(self.peers)

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

    @property
    def __str__(self):
        return ('-' * 4 + 'peers' + 4 * '-' + '\n'
                + ''.join([str(p) + '\n' for p in self.peers])
                + 13 * '-' + '\n')


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
            client.start_execution()
            break
            # client.update_peers(data)
            # client.broadcast(client.peers)
            # client.start_execution()
            # when current server can't be reached (disabled) it picks
            # one peer and makes a server out of that peer
        except ConnectionResetError:
            print(f'Connection Reset Error Occured\n{client.__str__}')
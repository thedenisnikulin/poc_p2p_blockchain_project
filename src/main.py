import random
import time
import sys
# local
import config
from server import Server
from client import Client


if __name__ == '__main__':
    while 1:
        try:
            server = Server(config.SERVER_ADDR, config.SERVER_PORT)
            server.run()
        except KeyboardInterrupt:
            sys.exit()
        except OSError:
            pass

        try:
            client = Client(config.SERVER_ADDR, config.SERVER_PORT)
            client.connect()
        except ConnectionResetError:
            # if current server can't be reached (connection reset)
            # pick one client and make a server out of it
            pass
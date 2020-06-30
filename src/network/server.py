import socket
from .config import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), PORT))
sock.listen(5)

while 1:
    client, address = sock.accept()
    print(f'connected to {address}')
    msg = client.recv(1024)
    print(msg.decode())
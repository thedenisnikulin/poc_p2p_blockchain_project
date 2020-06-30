import socket
import threading
from .config import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), PORT))

def send_msg():
    msg = input('msg: ')
    client.send((bytes(msg, 'utf-8')))

t = threading.Thread(target=send_msg)
t.start()
import socket


SERVER_ADDR = socket.gethostname()
SERVER_PORT = 9090
PORT_RANGE = (9000, 9100)
BUFF_SIZE = 4096  # 4096 because I saw that on stack overflow, lol

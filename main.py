import threading
import socket

host = '[IP_Address]'
port = 55555

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser
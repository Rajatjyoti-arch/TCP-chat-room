import threading
import socket

host = '[IP_Address]'
port = 55555

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def boradcast(message):
    for client in clients:
        client.send(message)
    
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            boradcast(message)
        except:
            index = client.index(client)
            client.remove(client)
            client.close()
            alias = aliases[index]
            aliases.remove(alias)
            boradcast(f'{alias} has left the chat'.encode('ascii'))
            break
    
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('alias?'.encode('ascii'))
        alias = client.recv(1024).decode('ascii')
        alias

        
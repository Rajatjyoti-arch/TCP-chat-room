import threading
import socket

alias = input("Choose your alias: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("[IP_Address]", 55555))

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'alias?':
               
            else:
                print(message)
        except:
            print("An error occured!")
            client.closed()
            break
            
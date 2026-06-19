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
               client.send(alias.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.closed()
            break
            
def write():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
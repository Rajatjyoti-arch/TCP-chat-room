import threading
import socket

alias = input("Choose your alias: ")
password = input("Enter elder password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("[IP_Address]", 55555))

stop_thread = False

def recieve():
    global stop_thread
    while True:
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'role?':
                client.send('elder'.encode('ascii'))
            elif message == 'alias?':
                client.send(alias.encode('ascii'))
            elif message == 'pass?':
                client.send(password.encode('ascii'))
            elif message == 'REFUSE':
                print("Connection was refused! Wrong password!")
                stop_thread = True
                client.close()
            elif message == 'BANNED':
                print("Connection refused! You are banned from this server!")
                stop_thread = True
                client.close()
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
            
def write():
    while True:
        if stop_thread:
            break
        try:
            msg = input("")
            if stop_thread:
                break
                
            if msg.startswith('/'):
                if msg.startswith('/kick '):
                    client.send(f'KICK {msg[6:]}'.encode('ascii'))
                else:
                    print("Elders can only use /kick command!")
            else:
                message = f'{alias}: {msg}'
                client.send(message.encode('ascii'))
        except:
            break

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

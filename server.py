import threading
import socket

host = '[IP_Address]'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []
roles = []
banned_ips = []

def boradcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def kick_user(name):
    if name in aliases:
        name_index = aliases.index(name)
        client_to_kick = clients[name_index]
        
        clients.remove(client_to_kick)
        aliases.remove(name)
        roles.pop(name_index)
        
        try:
            client_to_kick.send('You were kicked by an admin/elder!'.encode('ascii'))
        except:
            pass
        client_to_kick.close()
        
        boradcast(f'{name} was kicked!'.encode('ascii'))

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            
            msg_decoded = message.decode('ascii')
            
            if msg_decoded.startswith('KICK'):
                role = roles[clients.index(client)]
                if role in ['admin', 'elder']:
                    name_to_kick = msg_decoded[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
                    
            elif msg_decoded.startswith('BAN'):
                role = roles[clients.index(client)]
                if role == 'admin':
                    name_to_ban = msg_decoded[4:]
                    if name_to_ban in aliases:
                        name_index = aliases.index(name_to_ban)
                        client_to_ban = clients[name_index]
                        ip_addr = client_to_ban.getpeername()[0]
                        banned_ips.append(ip_addr)
                        kick_user(name_to_ban)
                        boradcast(f'{name_to_ban} was banned!'.encode('ascii'))
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                boradcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                aliases.remove(alias)
                roles.pop(index)
                boradcast(f'{alias} has left the chat'.encode('ascii'))
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        if address[0] in banned_ips:
            client.send('BANNED'.encode('ascii'))
            client.close()
            continue

        client.send('role?'.encode('ascii'))
        role = client.recv(1024).decode('ascii')
        
        if role == 'admin':
            client.send('pass?'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        elif role == 'elder':
            client.send('pass?'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'elderpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        client.send('alias?'.encode('ascii'))
        alias = client.recv(1024).decode('ascii')

        roles.append(role)
        aliases.append(alias)
        clients.append(client)

        print(f"Alias of client is {alias} (Role: {role})")
        boradcast(f"{alias} ({role}) has joined the chat!".encode("ascii"))
        client.send("Connected to server!".encode("ascii"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is listening...') 
recieve()

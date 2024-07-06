import threading
import socket
import random

host='127.0.0.1'
port=59000
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
aliases=[]
escaped=[]
L=random.randint(1,100)
R=random.randint(101,500)
guess=random.randint(L,R)

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    global L, R, guess
    while True:
        try:
            client.send(f'Server:Enter a guess between {L} and {R}'.encode('utf-8'))
            message=client.recv(1024).decode('utf-8')
            index=clients.index(client)

            if message.isdigit():
                num=int(message)
                if num==guess:
                    client.send("Server:You guessed it correct!!".encode('utf-8'))
                    clients.remove(client)
                    client.close()
                    alias=aliases[index]
                    escaped.append(alias)
                    broadcast(f'Server:{alias} has escaped the jail'.encode('utf-8'))
                    print(f'Server:{alias} has escaped the jail'.encode('utf-8'))
                    aliases.remove(alias)
                    break
                elif(num<L or num>R):
                    client.send("Server:You guess is out of range...".encode('utf-8'))
                elif(num>guess):
                    R=num-1
                    client.send(f"Server:Too high! New range: {L} - {R}".encode('utf-8'))
                else:
                    L=num+1
                    client.send(f"Server:Too Low! New range: {L} - {R}".encode('utf-8'))
            else:        
                client.send("Server:Please enter a valid number.".encode('utf-8'))
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            alias=aliases[index]
            broadcast(f'Server:{alias} has left the chat room'.encode('utf-8'))
            aliases.remove(alias)
            break

def recieve():
    print('Server is Running and  Listening on port.....')
    print(f'The guess Number to escape is {str(guess)}')
    while True:
        client,address=server.accept()
        print(f'Connection established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias=client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'Server:{alias} has Joined The Jail'.encode('utf-8'))
        client.send('Server:You are now connected!'.encode('utf-8'))
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__=="__main__":
    recieve()
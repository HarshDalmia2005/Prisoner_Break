import threading
import socket

alias=input('Choose an alias >>>')
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',59000))

def client_recieve():
    while True:
        try:
            message=client.recv(1024).decode('utf-8')
            if message=='alias?':
                client.send(alias.encode('utf-8'))
            elif(message=="Server:You guessed it correct!!"):
                print(message)
                client.close()
                break
            else:
                print(message)
        except:
            print('Error')
            client.close()
            break

def client_send():
    while True:
        try:
            message = input('')    
            client.send(message.encode('utf-8'))
                
        except Exception as e:
            print(f'Error: {e}')
            client.close()
            break

recieve_thread=threading.Thread(target=client_recieve)
recieve_thread.start()

send_thread=threading.Thread(target=client_send)
send_thread.start()
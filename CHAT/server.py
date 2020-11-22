import socket
import threading

SERVER="192.168.1.5"
PORT=7070
FORMATE="utf-8"

clients=[]
nicknames=[]

server=socket.socket()
server.bind((SERVER,PORT))
server.listen()

def borad_cast(message):
    for client in clients:
        client.send(message)


def receive():
    while True:
        client,addr=server.accept()
        print(f"[NEW CONNECTION WITH]: {addr}")
        client.send("choose your nickname".encode(FORMATE))
        nickname=client.recv(1024).decode(FORMATE)
        nicknames.append(nickname)
        clients.append(client)
        borad_cast(f'new shity just connected {nickname}'.encode(FORMATE))
        thread=threading.Thread(target=handle_client,args=(client,addr))
        thread.start()

def handle_client(client,addr):
    while True:
            message=client.recv(1024)
            if(message.decode(FORMATE)=="dis me"):
                index=clients.index(client)
                clients.remove(client)
                nickname=nicknames[index]
                borad_cast(f'shity idot {nickname} has just took off'.encode(FORMATE))
                nicknames.remove(nickname)
                break
            borad_cast(message)
    client.close()

print("[statring] server starting ...")
receive()

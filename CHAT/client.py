import socket
import threading

SERVER="192.168.1.5"
PORT=7070
FORMATE="utf-8"
client=socket.socket()
client.connect((SERVER,PORT))

NICKNAME=input("choose nick name:")

def recevie():
    while True:
        try:
            message=client.recv(1024).decode(FORMATE)
            if message =="choose your nickname":
                client.send(NICKNAME.encode(FORMATE))
            else:
                print(message)
        except:
            print("shity user cannot handel him self")
            client.close()
            break


def send():
    while True:
        message=input()
        full_message=f"{NICKNAME}:{message}"
        if(message=="dis me"):
            client.send(message.encode(FORMATE))
            client.close()
            break
        client.send(full_message.encode(FORMATE))

recevie_thread=threading.Thread(target=recevie)
recevie_thread.start()

send_thread=threading.Thread(target=send)
send_thread.start() 


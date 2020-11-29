import socket
import threading

SERVER="192.168.1.5"
PORT=7070
FORMATE="utf-8"
client=socket.socket()
client.connect((SERVER,PORT))

NICKNAME=input("choose nick name:")
if NICKNAME =="admin":
    password=input("enter the password: ")

stop_thread=False
def recevie():
    global stop_thread  
    while True:
        if stop_thread:
            break
        try:
            message=client.recv(1024).decode(FORMATE)
            if message =="choose your nickname":
                client.send(NICKNAME.encode(FORMATE))
                if NICKNAME=="admin":
                    next_message=client.recv(1024).decode(FORMATE)
                    if next_message =="password":
                        client.send(password.encode(FORMATE))
                        if client.recv(1024).decode(FORMATE) =="Wrong password":
                            print("Wrong password, imposter")
                            stop_thread=True
                    elif next_message =="YOU HAD A BAAAAAAN":
                        print("no chat for you")
                        client.close()
                        stop_thread=True
            else:
                print(message)
        except:
            print("shity user cannot handel him self")
            client.close()
            break


def send():
    while True:
        if stop_thread:
            break
        message=input()
        full_message=f"{NICKNAME}:{message}"

        if NICKNAME=="admin" and (message[:4] =="KICK" or  message[:3]=="BAN"):
            if message[:4] =="KICK":
                client.send(f"KIK {message[5:]}".encode(FORMATE))
                continue

            elif message[:3]=="BAN":
                client.send(f"BAN {message[4:]}".encode(FORMATE))
                continue

        if(message=="dis me"):
            client.send(message.encode(FORMATE))
            client.close()
            break

        client.send(full_message.encode(FORMATE))


"""
i/o is blocking by diffult so we use two function one for recive and one for send ,to not get blocked by the 
send and recive operation if we do it in same function (e.g if we now on the line that send so we cannot recivce 
untill we send) but here we use two function one for send and one for recieve,and each function run on a thread 
so the both can be perfomed any time
"""
recevie_thread=threading.Thread(target=recevie)
recevie_thread.start()

send_thread=threading.Thread(target=send)
send_thread.start() 


import socket
import threading
from tkinter import *

SERVER="192.168.1.5"
PORT=7070
FORMATE="utf-8"
client=socket.socket()
client.connect((SERVER,PORT))

NICKNAME=input("choose nick name:")
if NICKNAME =="admin":
    password=input("enter the password: ")

WINDOW=Tk()
WINDOW.title(NICKNAME)
WINDOW.resizable(False,False)

TxtInMessage=Text(WINDOW,width=50)
TxtInMessage.grid(row=0,column=0,padx=10,pady=10)

TxtOutMessage=Entry(WINDOW,width=50)
TxtOutMessage.insert(0,"Your message")
TxtOutMessage.grid(row=1,column=0,padx=10,pady=10)

        

stop_thread=False

def recevie():
    while True:
        global stop_thread  
        if stop_thread:
            break
        try:
            message=client.recv(1024).decode(FORMATE)
            if message =="choose your nickname":
                client.send(NICKNAME.encode(FORMATE))
                next_message=client.recv(1024).decode(FORMATE)
                if next_message =="password":
                    client.send(password.encode(FORMATE))
                    if client.recv(1024).decode(FORMATE) =="Wrong password":
                        TxtInMessage.insert(END,"\n"+"Wrong password Imposter")
                        stop_thread=True
                elif next_message =="YOU HAD A BAAAAAAN":
                    TxtInMessage.insert(END,"\n"+"no chat for you")
                    client.close()
                    stop_thread=True
            else:
                if(message==f"{NICKNAME}: Your message"):
                    message="You are now connected.."
                TxtInMessage.insert(END,"\n"+message)
        except:
            print("shity user cannot handel him self")
            WINDOW.destroy()
            client.close()
            break


def send():
    message=TxtOutMessage.get()
    full_message=f"{NICKNAME}: {message}"

    if NICKNAME=="admin" and (message[:4] =="KICK" or  message[:3]=="BAN" or message[:5]=="UNBAN"):
        if message[:4] =="KICK":
            client.send(f"KICK {message[5:]}".encode(FORMATE))

        elif message[:3]=="BAN":
            client.send(f"BAN {message[4:]}".encode(FORMATE))

        elif message[:5]=="UNBAN":
            client.send(f"UNBAN {message[6:]}".encode(FORMATE))
    else:
        client.send(full_message.encode(FORMATE))


    if(message=="dis me"):
        client.send(message.encode(FORMATE))
        client.close()

btnSendMessgage=Button(WINDOW,text="send",width=20,command=send)
btnSendMessgage.grid(row=2,column=0,padx=10,pady=10)
"""
i/o is blocking by default so we use two function one for recive and one for send ,to not get blocked by the 
send and recive operation if we do it in same function (e.g if we now on the line that send so we cannot recivce 
untill we send) but here we use two function one for send and one for recieve,and each function run on a thread 
so the both can be perfomed any time
"""



recevie_thread=threading.Thread(target=recevie)
recevie_thread.start()

send_thread=threading.Thread(target=send)
send_thread.start() 
WINDOW.mainloop()


import socket

HEADER=64
PORT=5050
SERVER="192.168.1.5"
FORMAT="utf-8"
DISCONNET="dis"
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

"""
send and recv: operates on the network buffer ,send return when you send the message and recv only return when the
size of the buffer you specify is filled,(VERY IMPORTANT: SEND ONLY SEND WHEN THE BUFFER YOU SPECIFIED ARE FILLED AND 
RECV ONLY RETURN WHEN THE BUFFER HAS BEEN EMPTYED) 
"""

"""
1-encode the message
2-get the length of the message(int)
3-convert that into string and endcode it
4-padding that length if it less that 64 bytes 
5-send the length of that message
6-send the actual message
"""
def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+= b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    #print(client.recv(2048).decode(FORMAT))

connect=True
while connect:
    s=input()
    if(s==DISCONNET):
        connect=False
    send(s)
    #client.close()

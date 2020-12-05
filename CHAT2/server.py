import socket
import threading

SERVER="192.168.1.5"
PORT=7070
FORMATE="utf-8"
PASSWORD="azxc"

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
        try:
            nickname=client.recv(1024).decode(FORMATE)   
        except :
            client.close()
            print("malicious clien disconnected")
            continue
            
        with open('ban.txt','r') as h:
            bans=h.readlines()
             
        if nickname+'\n' in bans:
            client.send("YOU HAD A BAAAAAAN".encode(FORMATE))
            client.close()
            continue

        if nickname =="admin":
            client.send("password".encode(FORMATE))
            password=client.recv(1024).decode(FORMATE)

            if password != PASSWORD:
                client.send("Wrong password".encode(FORMATE))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)
        borad_cast(f'new shity just connected {nickname}'.encode(FORMATE))
        thread=threading.Thread(target=handle_client,args=(client,addr))
        thread.start()

def handle_client(client,addr):
    while True:
        try:
            msg = message = client.recv(1024)
            if(msg.decode(FORMATE).startswith("KICK")):
                if nicknames[clients.index(client)] =="admin":  
                    name_to_kick=msg.decode(FORMATE)[5:]
                    print(name_to_kick)
                    print(msg.decode(FORMATE))
                    kick_user(name_to_kick)
                else:
                    client.send("this command for admin only".encode(FORMATE))

            elif(msg.decode(FORMATE).startswith("BAN")):
                if nicknames[clients.index(client)] =="admin":  
                    name_to_Ban=msg.decode(FORMATE)[4:]
                    kick_user(name_to_Ban)

                    with open('ban.txt','a')as h:
                        h.write(f"{name_to_Ban}\n")
                else:
                    client.send("this command for admin only".encode(FORMATE))

            elif(msg.decode(FORMATE).startswith("UNBAN")):
                if nicknames[clients.index(client)] =="admin":  
                    name_to_unBan=msg.decode(FORMATE)[6:]
                    print(name_to_unBan)
                    with open("ban.txt", "r+") as f:
                        lines = f.readlines()
                        f.seek(0)
                        print(lines)
                        for line in lines:
                            if line != name_to_unBan+"\n":
                                f.write(line)
                        f.truncate()
                else:
                    client.send("this command for admin only".encode(FORMATE))


            elif(message.decode(FORMATE)=="dis me"):
                index=clients.index(client)
                clients.remove(client)
                nickname=nicknames[index]
                borad_cast(f'shity idot {nickname} has just took off'.encode(FORMATE))
                nicknames.remove(nickname)
                break
            else:
                borad_cast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            nickname=nicknames[index]
            borad_cast(f'shity idot {nickname} has just took off'.encode(FORMATE))
            nicknames.remove(nickname)
            break

def kick_user(user):
    if user in nicknames:
        name_index=nicknames.index(user)
        client_to_kick=clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("NEXT TIME ... there is not next time :)".encode(FORMATE))
        client_to_kick.close()  
        nicknames.remove(user) 
        borad_cast(f"{user} get his ass kicked".encode(FORMATE))







print("[statring] server starting ...")
receive()

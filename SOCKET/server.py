
import socket
import threading

HEADER=64
PORT=5050
SERVER="192.168.1.5"
SERVER1=(socket.gethostbyname_ex(socket.gethostname())[2][1]) #get the divice public ip
ADDR=(SERVER,PORT)
FORMAT="utf-8"
DISCONNET="dis"


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#af ip address family inet->ipv4 and socket_stream is tcp sock_dgram is udp
server.bind(ADDR) #bind the socket to address take tuple of the address and the port we want to be bind to


"""
first message that get send is the lengt of the message that have to be 64 byte ,we padding it in the client side 
to be 64 because send and recv must known the size of the buffer so its 64,then the actual message get recived ,
wich is the size of the length we get after converting it back to int that get ride of extra padding and gives 
us the number that we will but in the recv(msg_length) to return after reading this message 
"""
def handle_client(conn,addr):
    print(f"[NEW CONNCETION]{addr}")
    conneted =True
    while conneted:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNET:
                conneted = False
                print("DISCONNETED!")
                break
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()




def logic():
    server.listen()
    print(f"[LISITING] server is listing on {SERVER}")
    while True:
        #socket liseten and via accept function and return tuple of new socket  object usable to send and recive date
        #on that connetion and  the other is a tuple that contatin the address of the socket trying to connect and 
        #the port numbre of that socket (new_socket,(address,port))
        conn,addr=server.accept()
        #create new thread and the target is handle client function so that the fucntion that the thread will run
        #and the arg that that function take is new socket and the address of the client
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        #get the number of active thread by diffult there is always one thread that is the start that listing 
        #to the encoming requests
        print(f"[ACTIVE CONNECTION] {threading.activeCount()-1}")
        


print("[statring] server starting ...")
logic()


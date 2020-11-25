from socket import *
def createServer():
    serversocket = socket(AF_INET,SOCK_STREAM)
    try :
        serversocket.bind(('localhost',9000))
        serversocket.listen()
        while(1):
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            if ( len(pieces) > 0 ) : print(pieces[0])
            """
            HTTP/1.1 200 OK
            Content-Type: text/html; charset=utf-8
            
            hey 
            your address and port is {address}
            """
            header  = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/plain; charset=utf-8\r\n"
            header += "\r\n"
            data =header+"hey\r\n"
            clientsocket.sendall(data.encode())
            data2=f"your address and port is {address}"
            clientsocket.sendall(data2.encode())
            clientsocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)

    serversocket.close()

print('Access http://localhost:9000')
createServer()

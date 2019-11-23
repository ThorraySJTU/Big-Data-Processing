from socket import *
import datetime
import threading
class client():
    def __init__(self, server_port):
        self.port = server_port
        self.client_id = None
        self.socket = None

    def __connect_server__(self, hostname, server_port):
        print("Start to connect with server")
        server_socket = socket(AF_INET,SOCK_STREAM)
        server_socket.connect((hostname,server_port))
        self.socket = server_socket
        print("Hello Server!")
        senddata = "Client"
        server_socket.sendall(senddata.encode())
        print("\nClient send data")
        data = server_socket.recv(1024).decode('utf-8')
        print(data)
        if data.split(":")[0] == "Client id ":
            client_id = int(data.split(":")[1])
        return server_socket, client_id

    def __status__(self, server_socket):
        senddata = "Status"
        add_info  = input("Lockname >>")
        senddata = "Status:"+add_info
        server_socket.sendall(senddata.encode())
        print("Check the lock status")
        data = server_socket.recv(1024).decode('utf-8')
        print(data) 

    def __lock__(self, server_socket):
        senddata = "Lock"
        add_info  = input("Lockname >>")
        senddata = "Lock:"+add_info
        server_socket.sendall(senddata.encode())
        print("Lock operation")
        data = server_socket.recv(1024).decode('utf-8')
        print(data) 

    def __release__(self, server_socket):
        senddata = "Release"
        add_info  = input("Lockname >>")
        senddata = "Release:"+add_info
        server_socket.sendall(senddata.encode())
        print("Release operation")
        data = server_socket.recv(1024).decode('utf-8')
        print(data) 

    def lock_request(self,server_socket):
        while True:
            LockRequest = input("Please enter your command:")
            if LockRequest == "Status":
                self.__status__(server_socket)
                continue
            elif LockRequest == "Lock":
                self.__lock__(server_socket)
                continue
            elif LockRequest == "Release":
                self.__release__(server_socket)
                continue
            else:
                print(LockRequest,"is not a valid request. Please entre Status/Lock/Release.")

    def run(self):
        hostname = '127.0.0.1'
        port = self.port
        server_socket, client_id = self.__connect_server__(hostname,port)
        print("Server socket:",server_socket," client id",client_id)
        self.lock_request(server_socket)

#client = client(9005)
#client.run() 
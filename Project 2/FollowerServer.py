from socket import *
import threading
from threading import Thread
class FollowerServer():
    def __init__(self, self_port, leaderserver_port):
        self.self_port = self_port
        self.leader_port = leaderserver_port
        self.client = []
        self.follower_id = None

    def __new_client__(self,client_socket):
        client_id = self.follower_id * 50000 + len(self.client)
        self.client.append(({"client id":client_id,"socket":client_socket}))
        return client_id

    def __connect_with_leaderserver__(self, host, port):
        print("Start to connect with leader_server")
        leader_socket = socket(AF_INET,SOCK_STREAM)
        leader_socket.connect((host, port))
        senddata = "Follower"
        leader_socket.sendall(senddata.encode())
        print("\nFollower send data")
        data = leader_socket.recv(1024).decode('utf-8')
        if data.split(":")[0] == "Follower id ":
            follower_id = int(data.split(":")[1])
            self.follower_id = follower_id
        return leader_socket, follower_id
    def __connect_with_client__(self, client_socket,res_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                continue
            if data == "Client":
                client_id = self.__new_client__(client_socket)
                client_socket.sendall(("Client id :%d"%(client_id)).encode())
                continue
            if data == "Status":
                res_socket.sendall("Status".encode())
                data = res_socket.recv(1024).decode('utf-8')
                client_socket.sendall(data.encode())
            if data == "Lock":
                res_socket.sendall("Lock".encode())
                data = res_socket.recv(1024).decode('utf-8')
                client_socket.sendall(data.encode())
            if data == "Release":
                res_socket.sendall("Status".encode())
                data = res_socket.recv(1024).decode('utf-8')
                client_socket.sendall(data.encode())



    
    def run(self):
        host = '127.0.0.1'
        leader_socket, follower_id = self.__connect_with_leaderserver__(host, self.leader_port)
        print("Connect with leader server !")


        s = socket(AF_INET,SOCK_STREAM)
        s.bind((host, self.self_port))
        s.listen(3)
        print(s,"Listening!")

        while True:
            client_socket, addr = s.accept()
            print("Connect with client:", addr)
            connect_with_client = threading.Thread(target=self.__connect_with_client__,args=(client_socket,leader_socket,))
            connect_with_client.setDaemon(True)
            connect_with_client.start()

#follower = FollowerServer(9005,9000)
#follower.run() 

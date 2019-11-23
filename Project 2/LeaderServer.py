from socket import *
import threading
from threading import Thread
class LeaderServer():
    def __init__(self,port):
        self.port = port
        self.client = []
        self.connection = []
        self.FollowerServer = []
        self.lock_map = []
    
    def __new_client__(self,res_socket):
        client_id = len(self.client) + 50000
        self.client.append(({"client id":client_id,"socket":res_socket}))
        return client_id

    def __new_follower__(self,res_socket):
        follower_id = len(self.FollowerServer) + 2
        self.FollowerServer.append({"follower_id":follower_id,"socket":res_socket})
        return follower_id
    
    def __lock_map__(self):
        print(self.lock_map)
        length_lock_map = len(self.lock_map)
        return length_lock_map

    def __lock__(self,res_socket):
        print(self.lock_map)
        length_lock_map = len(self.lock_map)
        if length_lock_map == 0:
            self.lock_map.append(res_socket)
            print(self.lock_map)
        else:
            length_lock_map = 2
        return length_lock_map

    def __release__(self,res_socket):
        print(self.lock_map)
        length_lock_map = len(self.lock_map)
        if length_lock_map == 1:
            if res_socket == self.lock_map[0]:
                self.lock_map = []
                print(self.lock_map)
            else:
                length_lock_map = 2
        else:
            length_lock_map = 0
        return length_lock_map


    def __response__(self,res_socket):
        while True:
            data = res_socket.recv(1024).decode('utf-8')
            #print(data)
            if not data:
                continue
            if data == "Client":
                print(data)
                client_id = self.__new_client__(res_socket)
                res_socket.sendall(("Client id :%d"%(client_id)).encode())
                continue
            if data == "Follower":
                follower_id = self.__new_follower__(res_socket)
                res_socket.sendall(("Follower id :%d"%(follower_id)).encode())
                continue
            if data == "Status":
                print(data)
                lock_map = self.__lock_map__()
                if lock_map == 0:
                    res_socket.sendall("Release".encode())
                else:
                    res_socket.sendall("Lock".encode())
            if data == "Lock":
                print(data)
                lock_map = self.__lock__(res_socket)
                print(lock_map)
                if lock_map == 0:
                    res_socket.sendall("Lock".encode())
                if lock_map == 2:
                    res_socket.sendall("You can't lock.".encode())
            if data == "Release":
                print(data)
                lock_map = self.__release__(res_socket)
                print(lock_map)
                if lock_map == 1:
                    res_socket.sendall("Release".encode())
                if lock_map == 2:
                    res_socket.sendall("The owner of the lock is not you.".encode())
                if lock_map == 0:
                    res_socket.sendall("There isn't a lock".encode())
                
    
    def run(self):
        host = '127.0.0.1'
        port = self.port
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((host,port))
        s.listen(5)
        print(s)

        while True:
            print("Listening....")
            conn_socket, addr = s.accept()
            print("Connect from : ", addr)
            self.connection.append(conn_socket)
            leader_server_thread = threading.Thread(target=self.__response__, args = (conn_socket,))   
            leader_server_thread.setDaemon(True)
            leader_server_thread.start()
            print("active threads:")
            print(threading.active_count())

LeaderServer = LeaderServer(9000)
LeaderServer.run()
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
        self.lock_name = []
    
    def __new_client__(self,res_socket):
        client_id = len(self.client) + 50000
        self.client.append(({"client id":client_id,"socket":res_socket}))
        return client_id

    def __new_follower__(self,res_socket):
        follower_id = len(self.FollowerServer) + 2
        self.FollowerServer.append({"follower_id":follower_id,"socket":res_socket})
        return follower_id
    
    def __lock_map__(self,res_socket,msg):
        print(self.lock_map)
        print(self.lock_name)
        try:
            index = self.lock_name.index(msg)
            info = self.lock_map[index]
        except:
            info = ""
        return info

    def __lock__(self,res_socket,msg):
        print(self.lock_map)
        print(self.lock_name)
        flag = 0
        for i in self.lock_map:
            if i == res_socket:
                flag = 1
        if flag == 0:
            for i in self.lock_name:
                if i == msg:
                    flag = 2
            if flag == 0:
                self.lock_map.append(res_socket)
                self.lock_name.append(msg)
        return flag

    def __release__(self,res_socket,msg):
        print(self.lock_map)
        length_lock_map = len(self.lock_map)
        flag = 0
        for i in self.lock_map:
            if i == res_socket:
                flag = 1
        if length_lock_map != 0:
            if flag == 1:
                if self.lock_map.index(res_socket) == self.lock_name.index(msg):
                    self.lock_map.remove(res_socket)
                    self.lock_name.remove(msg)
                else:
                    flag = 2
            else:
                flag = 2
        else:
            flag = 0
        return flag


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
            if data.split(":")[0] == "Status":
                print("Data is Status:",data)
                msg = data.split(":")[1]
                lock_map = self.__lock_map__(res_socket,msg)
                print(lock_map)
                if lock_map == "":
                    res_socket.sendall(("There isn't a lock named>>"+msg).encode())
                else:
                    res_socket.sendall((msg+">>Lock Status\nOwner information: "+str(lock_map)).encode())
                
            if data.split(":")[0] == "Lock":
                print("Data is Lock:",data)
                msg = data.split(":")[1]
                lock_map = self.__lock__(res_socket,msg)
                print(lock_map)
                if lock_map == 0:
                    res_socket.sendall((msg+">>Lock Status").encode())
                if lock_map == 1:
                    res_socket.sendall(("You have already had a Lock !").encode())
                if lock_map == 2:
                    res_socket.sendall((msg+">>This name of Lock have existed.").encode())
            if data.split(":")[0] == "Release":
                print("Data is Release:",data)
                msg = data.split(":")[1]
                print(res_socket)
                lock_map = self.__release__(res_socket,msg)
                print(lock_map)
                if lock_map == 1:
                    res_socket.sendall((msg+">>Release Status").encode())
                if lock_map == 2:
                    res_socket.sendall(("You don't have a lock named>>"+msg).encode())
                if lock_map == 0:
                    res_socket.sendall(("There isn't any lock.").encode())
                
    
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
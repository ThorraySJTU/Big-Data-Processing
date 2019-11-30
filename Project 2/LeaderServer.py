from socket import *
import threading
from threading import Thread
class LeaderServer():
    def __init__(self,port):
        self.port = port
        self.client = []
        self.connection = []
        self.FollowerServer = []
        self.FollowerServerSocket = []
        self.lock_map = []
        self.lock_name = []
    
    def __new_client__(self,res_socket):
        client_id = len(self.client) + 50000
        self.client.append(({"client id":client_id,"socket":res_socket}))
        return client_id

    def __new_follower__(self,res_socket):
        follower_id = len(self.FollowerServer) + 2
        self.FollowerServer.append({"follower_id":follower_id,"socket":res_socket})
        self.FollowerServerSocket.append(res_socket)
        return follower_id
    
    def __lock_map__(self,msg):

        try:
            index = self.lock_name.index(msg)
            info = self.lock_map[index]
        except:
            info = ""
        return info

    def __lock__(self,msg,client_id):
        ##print(self.lock_map)
        ##print(self.lock_name)
        flag = 0
        for i in self.lock_map:
            if i == client_id:
                flag = 1
        if flag == 0:
            for i in self.lock_name:
                if i == msg:
                    flag = 2
            if flag == 0:
                self.lock_map.append(client_id)
                self.lock_name.append(msg)
        return flag

    def __release__(self,msg,client_id):
        #print(self.lock_map)
        length_lock_map = len(self.lock_map)
        flag = 0
        for i in self.lock_map:
            if i == client_id:
                flag = 1
        if length_lock_map != 0:
            if flag == 1:
                try:
                    if self.lock_map.index(client_id) == self.lock_name.index(msg):
                        self.lock_map.remove(client_id)
                        self.lock_name.remove(msg)
                    else:
                        flag = 2
                except:
                    flag = 2
            else:
                flag = 2
        else:
            flag = 0
        return flag


    def __response__(self,res_socket):
        while True:
            #if res_socket not in connectsocket:
                #connectsocket.append(res_socket)
            data = res_socket.recv(1024).decode('utf-8')
            #print(data)
            if not data:
                continue
            if data == "Client":
                #print(data)
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
                client_id = data.split(":")[2]
                lock_map = self.__lock_map__(msg)
                ##print(lock_map)
                if lock_map == "":
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode())  
                    res_socket.sendall(("There isn't a lock named>>"+msg).encode())                 
                else:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode()) 
                    res_socket.sendall((msg+">>Lock Status\nOwner information: "+lock_map).encode())  
                
            if data.split(":")[0] == "Lock":
                print("Data is Lock:",data)

                msg = data.split(":")[1]
                client_id = data.split(":")[2]
                lock_map = self.__lock__(msg,client_id)
                ##print(lock_map)
                if lock_map == 0:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Lock:"+client_id).encode())
                    res_socket.sendall((msg+">>Lock Status").encode())
                if lock_map == 1:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode())   
                    res_socket.sendall(("You have already had a Lock !").encode())
                if lock_map == 2:
                   
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode())   
                    res_socket.sendall((msg+">>This name of Lock have existed.").encode())
            if data.split(":")[0] == "Release":
                print("Data is Release:",data)
                msg = data.split(":")[1]
                ##print(res_socket)
                client_id = data.split(":")[2]
                lock_map = self.__release__(msg,client_id)
                
                ##print(lock_map)
                if lock_map == 1:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Release:"+client_id).encode())
                    res_socket.sendall((msg+">>Release Status").encode())

                if lock_map == 2:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode())   
                    res_socket.sendall(("You don't have a lock named>>"+msg).encode())
                if lock_map == 0:
                    
                    for socketName in self.FollowerServerSocket:
                        socketName.sendall((msg+":Pass:"+client_id).encode())   
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
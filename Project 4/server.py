import os
from socket import *
from time import ctime
import threading
from tree import *
import json

BUFSIZ = 1024


class DFSServer:  # server 收到client发送过来的指令并且执行。server会监听端口
    #server每次收到客户指令的时候，要send给所有的friends，让他们执行同样的指令——所有friend server的tree应该是保持一致的
    def __init__(self, addr, portno, user='User1'):
        self.port = portno
        self.addr = addr
        self.friends = []
        self.clients = []
        self.user = user
        self.root = TreeNode('root')
        self.order = ''
        self.root.add_child(TreeNode('home'))
        self.home = self.root.arrive_node('home')
        self.home.add_child(TreeNode('user'))
        self.directory = self.home.arrive_node('user')
    def bind_socket(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.addr, self.port))
        self.sock.listen(12)


    def receive(self):  # 收到指令并且执行

        while True:
            conn_socket, addr = self.sock.accept()
            print("Connect from : ", addr)
            #print('here')
            datarecv = conn_socket.recv(1024).decode('utf-8')  # 在这里server收到client发过来的命令
            if not datarecv:
                continue
            datatoread = json.loads(datarecv)
            tag = datatoread['tag']
            data = datatoread['data']
            print(tag,data)
            if tag=='friend':
                self.execute(data)
            elif tag == 'sender':
                result = self.execute(data)
                for friend in self.friends:
                    try: #尝试朋友是否已连接，并向所有的朋友发数据
                        #每次发命令之前，应该检查朋友的树和自己的树是不是一样的，如果不一样更新之

                        datosend = json.dumps({'tag':'friend','data':data})
                        self.send(friend, datosend)  # 把收到的命令发给每一个朋友让朋友也执行该命令
                    except ConnectionRefusedError as e:
                        print('friend collapsed, ',e)
                    finally:
                        conn_socket.sendall(result.encode())
            else:
                conn_socker.sendall('who are you'.encode())




    def send(self,friend,data):

        consock = socket(AF_INET,SOCK_STREAM)
        cc = consock.connect((friend.addr,friend.port))
        if cc ==0:
            print('a friend crush')
            return 'connection failed'
        consock.sendall(data.encode())



    def create_friend_socket(self, addr,portno): #和其他服务器通信，建立端口。在建立端口的时候互相发用户名
        print("Connecting with friends")

        friend_socket = socket(AF_INET,SOCK_STREAM)
        #friend_socket.connect((addr, portno))
        friend = DFSServer(addr,portno,user = self.user) #这里user这样写是有问题的，这样的话所有的server user得一样才行
        friend.sock = friend_socket

        self.friends.append(friend)



    def execute(self, data):
        commandlist = data.split()  # 默认split空格
        if commandlist[0] == 'ls':  # ls会有两种情况 ls xx/xx/xx 和 ls
            if len(commandlist)>1:  # case ls xx/xx/xx
                if len(commandlist) > 2:  # 不能 ls xx/xx/xx xxxxxx 只能 ls xx/xx/xx
                    res = "your command is unreal"
                real_commandlist = commandlist[1].split('/')
                # directory = self.directory
                tmp = self.directory.arrive_node(real_commandlist)
                if tmp == None:
                    res = 'no directory named '+ commandlist[1]
                else:
                    res = tmp.list_children()
            else:  # case ls
                res = self.directory.list_children()

        elif commandlist[0] == 'mkdir':  # mkdir 只有一种情况： mkdir xx
            if len(commandlist) > 2:  # 只能mkdir xx 所以 commandlist 长度只能=2
                res = 'your command is unreal'
            elif len(commandlist) == 1:
                res = 'please input the name of the folder that you want to create.'
            else:
                # 这里要判定要建立的文件夹名字是不是非法的
                illegal_list = ['/', '\\', '<', '>', ':', '*', '"', '?', '|']
                isillegal = 0
                for i in range(len(illegal_list)):  # 非法状况判定
                    if commandlist[1].find(illegal_list[i]) != -1:
                        isillegal = 1
                if isillegal == 1:
                    res = "your folder name is illegal"
                else:
                    res = ''
                    self.directory.add_child(TreeNode(commandlist[1]))

        elif commandlist[0] == 'touch': #touch其好像不止这一种情况不过更多的我也懒得写了
            if len(commandlist) > 2:  # 只能touch xx 所以 commandlist 长度只能=2
                res = 'your command is unreal'
            elif len(commandlist) == 1:
                res = 'please input the name of the file that you want to create.'
            else:
                # 这里要判定要建立的文件名字是不是非法的
                illegal_list = ['/', '\\', '<', '>', ':', '*', '"', '?', '|']
                fileillegal = 0
                for i in range(len(illegal_list)):  # 非法状况判定
                    if commandlist[1].find(illegal_list[i]) != -1:
                        fileillegal = 1
                if fileillegal == 1:
                    res = "your folder name is illegal"
                else:
                    res = ''
                    self.directory.add_child(commandlist[1])


        elif commandlist[0] == 'rm':
            if len(commandlist) > 2:
                res = 'your command is unreal'
            elif len(commandlist) == 1:
                res = 'name required'
            else:
                res = ''
                self.directory.del_child(commandlist[1]) # a faire

        elif commandlist[0] == 'tree':
            #res = '反正是个树'
            res = self.root.show_tree()
        elif commandlist[0] == 'pwd':
            res = self.directory.print_path()

        elif commandlist[0] == 'cd':
            if len(commandlist) > 2:
                res = 'your command is unreal'
            elif len(commandlist) == 1:
                res = 'directory needed'
            else:
                # 先把乌七八糟的情况都去掉
                if commandlist[1] == '..':
                    tmp = self.directory.parent
                    if tmp == None:
                        res = "Don't tap cd .. in root!"
                    else:
                        res = ''
                        self.directory = tmp
                elif commandlist[1] == '~':
                    tmp = self.home.arrive_node('user')
                    res = ''
                    self.directory = tmp  # 这个是一定会有的
                elif commandlist[1] == '-':  # 我不想支持这个命令
                    res = "This file system do not support 'cd -'"

                else:  # 普通的情况
                    dicttogo = commandlist[1].split('/')
                    tmp = self.directory.arrive_node(dicttogo)
                    if tmp == None:
                        res = 'no such path'
                    else:
                        res = ''
                        self.directory = tmp
        else:
            res = 'your command is unreal'
        pp = str(self.directory.print_path())
        finalpp = str(res)+'\n'+pp
        #finalpp = res + '\0' + str(pp)
        #print (finalpp)
        return finalpp

    def getclientaddress(self,clinum):
        return self.clients[clinum].addr

    def addclient(self, cli, cli_addr):
        # addclient部分是需要查重的。
        newclient = DFSclient(cli, cli_addr)
        self.clients.append(newclient)

    def removeclient(self, cli):
        for i in range(len(self.clients)):
            if self.clients[i].name == cli:
                self.clients.remove(self.clents[i])
                print("client number ", i, " removed")

    def removeclient(self, addr):
        for i in range(len(self.clients)):
            if self.clients[i].addr == addr:
                self.clients.remove(self.clents[i])
                print("client number ", i, " removed")

    def run(self):
        #host = self.addr
        #port = self.port
        #s.bind((host, port))


        while True:
            print("Listening....")
            #self.connection.append(conn_socket)
            self.receive()
            #leader_server_thread = threading.Thread(target=self.receive(self.sock), args=(conn_socket))
            #leader_server_thread = threading.Thread(target=self.receive())
            #leader_server_thread.setDaemon(True)
            #leader_server_thread.start()
            #print("active threads:")
            #print(threading.active_count())


class DFSclient:  # client会发送指令给server让server执行。client不会监听端口
    def __init__(self, addr, portno,name):
        self.port = portno
        self.sock = socket(AF_INET,SOCK_STREAM)
        self.addr = addr
        self.name = name
        self.servers = []

    def __send__(self, addr, port,data):
        #print("Start to connect with server")
        self.sock = socket(AF_INET,SOCK_STREAM)
        self.sock.connect((addr,port))
        #print("Server connected")
        datosend = json.dumps({'tag':'sender','data':data})
        self.sock.sendall(datosend.encode())
        response = self.sock.recv(1024).decode('utf-8')
        print(response)

    def getsocketfd(self):
        return self.sock


if __name__ == '__main__':
    Myserver = DFSServer('127.0.0.1', 8889, user='user1')
    Myserver.bind_socket()
    Myserver.create_friend_socket('127.0.0.1', 9999)
    Myserver.run()

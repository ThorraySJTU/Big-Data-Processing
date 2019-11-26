import os
from socket import *
from time import ctime
import threading
from tree import *

BUFSIZ = 1024


class DFSServer:  # server 收到client发送过来的指令并且执行。server会监听端口
    def __init__(self, addr, portno, user='User1'):
        self.port = portno
        self.sock = ''
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

    def receive(self, sockno):  # 收到指令并且执行
        while True:
            data = sockno.recv(BUFSIZ).decode('utf-8')  # 在这里server收到client发过来的命令
            if not data:
                continue
            print(data)
            self.order = data
            self.execute(data)  # 执行收到的命令

    def execute(self, data):
        commandlist = data.split()  # 默认split空格
        if commandlist[0] == 'ls':  # ls会有两种情况 ls xx/xx/xx 和 ls
            if commandlist[1]:  # case ls xx/xx/xx
                if len(commandlist) > 2:  # 不能 ls xx/xx/xx xxxxxx 只能 ls xx/xx/xx
                    print("your command is unreal")
                real_commandlist = commandlist[1].split('/')
                # directory = self.directory
                tmp = self.directory.arrive_node(real_commandlist)
                if tmp == None:
                    print('no directory named ', commandlist[1])
                else:
                    tmp.list_children()
            else:  # case ls
                self.directory.list_children()

        elif commandlist[0] == 'mkdir':  # mkdir 只有一种情况： mkdir xx
            if len(commandlist) > 2:  # 只能mkdir xx 所以 commandlist 长度只能=2
                print('your command is unreal')
            elif len(commandlist) == 1:
                print('please input the name of the folder that you want to create.')
            else:
                # 这里要判定要建立的文件夹名字是不是非法的
                illegal_list = ['/', '\\', '<', '>', ':', '*', '"', '?', '|']
                isillegal = 0
                for i in range(len(illegal_list)):  # 非法状况判定
                    if commandlist[1].find(illegal_list[i]) != -1:
                        isillegal = 1
                if isillegal == 1:
                    print("your folder name is illegal")
                else:
                    self.directory.add_child(TreeNode(commandlist[1]))

        elif commandlist[0] == 'touch':
            if len(commandlist) > 2:  # 只能mkdir xx 所以 commandlist 长度只能=2
                print('your command is unreal')
            elif len(commandlist) == 1:
                print('please input the name of the file that you want to create.')
            else:
                # 这里要判定要建立的文件名字是不是非法的
                illegal_list = ['/', '\\', '<', '>', ':', '*', '"', '?', '|']
                fileillegal = 0
                for i in range(len(illegal_list)):  # 非法状况判定
                    if commandlist[1].find(illegal_list[i]) != -1:
                        fileillegal = 1
                if fileillegal == 1:
                    print("your folder name is illegal")
                else:
                    self.directory.add_child(commandlist[1])


        elif commandlist[0] == 'rm':
            if len(commandlist) > 2:
                print('your command is unreal')
            elif len(commandlist) == 1:
                print('name required')
            else:
                self.directory.del_child(commandlist[1])

        elif commandlist[0] == 'tree':
            self.root.show_tree()
        elif commandlist[0] == 'pwd':
            self.directory.print_path()

        elif commandlist[0] == 'cd':
            if len(commandlist) > 2:
                print('your command is unreal')
            elif len(commandlist) == 1:
                print('directory needed')
            else:
                # 先把乌七八糟的情况都去掉
                if commandlist[1] == '..':
                    tmp = self.directory.parent
                    if tmp == None:
                        print("Don't tap cd .. in root!")
                    else:
                        self.directory = tmp
                elif commandlist[1] == '~':
                    tmp = self.home.arrive_node(self.user)
                    self.directory = tmp  # 这个是一定会有的
                elif commandlist[1] == '-':  # 我不想支持这个命令
                    print("This file system do not support 'cd -'")

                else:  # 普通的情况
                    dicttogo = commandlist[1].split('/')
                    tmp = self.directory.arrive_node(dicttogo)
                    if tmp == None:
                        print('no such path')
                    else:
                        self.directory = tmp
        else:
            print('your command is unreal')
        return self.directory

    def getclientaddress(self,clinum):
        return self.clients[clinum].addr

    def addclient(self, cli, cli_addr):
        # addclient部分是需要查重的。
        newclient = client(cli, cli_addr)
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
        host = self.addr
        port = self.port
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        print(s)

        while True:
            print("Listening....")
            conn_socket, addr = s.accept()
            print("Connect from : ", addr)
            self.connection.append(conn_socket)
            leader_server_thread = threading.Thread(target=self.__response__, args=(conn_socket,))
            leader_server_thread.setDaemon(True)
            leader_server_thread.start()
            print("active threads:")
            print(threading.active_count())


class client:  # client会发送指令给server让server执行。client不会监听端口
    def __init__(self, addr, name):
        self.port = 8888
        self.sock = ''
        self.addr = addr
        self.name = name
        self.servers = [{'name': 'name', 'addr': '127.0.0.1'}]

    def readin(self):  # 这两个函数可能没有用
        print('readin')

    def writedown(self):
        print('writedown')

    def send(self, hostname, portno):
        hostaddr = ''
        for i in range(len(self.servers)):
            if self.servers[i]['name'] == hostname:
                hostaddr = self.servers[i]['addr']
            else:
                print("server does not exist")
                break
        print("connecting to port ", portno, " with server ", hostname)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(hostaddr)

        # a faire

    def getsocketfd(self):
        return self.sock


if __name__ == '__main__':
    Myserver = DFSServer('127.0.0.1', 8888, user='user1')
    Myserver.run()

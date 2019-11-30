from server import DFSclient,DFSServer

if __name__ == '__main__':
    Myserver2 = DFSServer('127.0.0.1', 9999, user='user1')
    Myserver2.bind_socket()
    Myserver2.create_friend_socket('127.0.0.1',8889)
    Myserver2.run()
from server import DFSclient,DFSServer
if __name__ == '__main__':
    client1 = DFSclient('127.0.0.1',8911,'user1')
    while True:
        order = input()
        client1.__send__('127.0.0.1',9999,order)

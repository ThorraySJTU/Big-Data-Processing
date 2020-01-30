# Introduction

tree.py defines the tree for DFS file system.

api.py defines functions for testing the tree, such as ls, cd, mkdir, rm, etc. 

server.py defines servers and clients for DFS. Where server could listen to a port, receive commands from clients and execute them in its file system.

server.py shall import tree.py, but not api.py. Functions in api.py are re-written to suit the server's format. 

server2.py used for running another server.

client.py and client2.py used for creating two clients following different servers. We could change the ip address and port in client*.py to change the server that it follows.

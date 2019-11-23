# Big Data Processing

## Project 2 Distributed Lock Design

Create 3 classes in LeaderServer.py/FollowerServer.py/Client.py

Leader server connect to follower server and client.

Follower server connect between leader server and client.

In version_2019_11_23_1, there is one lock. If someone preempts the lock, others can't release it. Everyone has the right to open the lock, as long as he locks it.

Everyone can check the status of the lock at any time.

### Use

```
python LeaderServer.py
```

```
python FollowerServer.py
```

```
python Client.py
```

```
python Client_leader.py
```

```
python Client_follower_1.py
```

You can add the command in the fourth and fifth terminal. (Status/Lock/Release)

Now, there is a problem. When we **Lock** in the client which connects directly to the leader server, the status of the lock, which connects to the follower server is wrong .

### To do

Solve the above problem.

Each client has its own lock, but not all users have one lock.


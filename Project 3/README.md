# Introduction

There are two files:
  * const_share.py: It defined several meta-parameters.
  * main.py: It defined several actions in our MiniDFS such as "put", "fetch", "read", "ls", and "quit".

In our MiniDFS, there are totally 4 repositories and each file will be duplicated for 3 times in different repositories.
If the file is larger than 2MB, it will be splited into peaces whose maximum size is 2MB.

# Functions:

  * put: Write a local file into our MiniDFS.
  * read: Read an assigned file for a special part.
  * fetch: Download the file in MiniDFS to local path.
  * ls: Get the file list of MiniDFS.
  * quit: Exit MiniDFS.

﻿**NOTE: THIS PACKAGE IS IN TEST VERSION YET.**

# EasyFTP

EasyFTP is a Python library that simplifies the process of interacting with FTP (File Transfer Protocol) servers. With EasyFTP, you can easily upload, download, delete, and list files and directories on remote FTP servers using a simple and intuitive interface.

## Features

- Connect to FTP servers with ease.
- Upload files and directories to remote servers.
- Download files and directories from remote servers.
- Delete files and directories on remote servers.
- List files and directories on remote servers.
- *(not implemented)* ~~Support for both FTP and secure FTP (FTPS).~~

## Installation

You can install EasyFTP via pip:

```bash
pip install EasyFTP
```

## Usage
 - Establishing connection
```py
from EasyFTP import EasyFTP as easyftp

with easyftp.EasyFTP() as session:
	session.connect("192.168.1.1", 21, "admin", "12345678", timeout = 30)
	# Change it to your option, and timeout is not necessary.
```
- Listing files on remote directory
```py
from EasyFTP import EasyFTP as easyftp

with easyftp.EasyFTP() as session:
	session.connect("192.168.1.1", 21, "admin", "12345678", timeout = 30)
	# Change it to your option, and timeout is not necessary.
	l = session.ls("/examples")
	# Directory argument is not necessary;
	# It will print structure of current directory when there is no argument.
	print(l)
```
It will print, for example: `["dir1", "dir2", "dir3", "example.py", "example.py2"]`

- Changing directory in remote (and printing current working directory)
```py
from EasyFTP import EasyFTP as easyftp

with easyftp.EasyFTP() as session:
	session.connect("192.168.1.1", 21, "admin", "12345678", timeout = 30)
	# Change it to your option, and timeout is not necessary.
	
	session.cd("/examples")
	# This will change your directory to /examples.
	# NOTE: Relative path is not tested yet.

	print(session.cd())
	# This will print "/examples", which is your current working directory.
	# It does this when there is no argument passed to it.

	print(session.pwd())
	# It works life session.cd() when there is no argument passed.
```


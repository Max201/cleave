Python Server Cleave
====================
**Server Cleave** package has some crossplatform solutions that can simplify socket server building as well as give some utilities like a Http File Server **serve** or **Encryprion Utility**. Writed a pretty clean and lightweight on a pure python2.7, that doesn't requires any external tools or libraries.

Install
-------

    pip install cleave


Requirements
------------
 - python2.7
 - python setuptools
 - python pip


**serve** tool
----------
After installation cleave, serve tool allows you to run simplest **Http File Server** in one command. *[dirname]* will be used as base directory. 

    $ serve [dirname]
    # Will serve your [dirname] directory on http://127.0.0.1:8008
    # And all files will be accessible by http://127.0.0.1:8008/[filename]
    

You can setup directory index file by setting up *[filename]*, in this case *[dirname]* will be a *[filename] directory*.

 - /home/proj/
    - css
        - custom.css
    - index.html
 
To get index.html even if you go to http://127.0.0.1:8008 (and not http://127.0.0.1:8008/index.html) you must specify index.html path.

    $ serve index.html
    # In this case base directory will be */home/proj/*
    # And if you go to http://127.0.0.1:8008 server should open index.html

### SERVER API: Quick start guide
Cleave api allows you to create lightweight socket servers. For example [Http File Server source](https://github.com/Max201/cleave/blob/master/cleave/tool/serve.py "Http File Server source"). This simple server can serve your local files using multithreading for requests, that allows you to get many files in parallel. All server class what you need are located in **cleave.server** package (BaseServer, BaseClient). Here is an example "how to use"

**test.py**
	
    # Import basic server classes
    from cleave import server
    
    # Extend test server from BaseServer
    class MyServer(server.BaseServer):
	    # When client connects to your server,
	    # he will send "hello world" message
        def client_handler(self, client):
            client.send('Hello world!')
    
    if __name__ == '__main__':
	    # Run server on "http://localhost:80" with maximum
	    # clients = 10
	    MyServer(host='localhost', port=80, clients=10)

Run your file from command line:

	python test.py
	

### Encryption Utility: Quick start guide
Encryption package allows you to encrypt / decrypt string in a simplest way. Library located in **cleave.encrypt** package ( Encrypt class ).

	# Import encryption library
	>>> from cleave.encrypt import Encrypt
	
	# Encrypt your string into md5
	>>> Encrypt("cleave").md5
	u'45503e6f0c8f26a483083b9c9a5b9298'
	
	# Double encryption
	>>> Encrypt("cleave").md5.md5
	u'e379bb20fd08ee4b403dbd3ad5b0f68a'

You can use following encryption algorithms:

- md5
- crc32
- base16 / unbase16
- base64 / unbase64
- sha1 / sha224 / sha256 / sha384 / sha512

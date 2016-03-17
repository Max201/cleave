Python Server Cleave
====================

Install
-------

    pip install cleave


Requirements
------------
 - python2.7
 - python setuptools
 - python pip

How to use
----------
**test.py**
	
    from cleave import server
    
    class MyServer(server.BaseServer):
        def client_handler(self, client):
            client.send('Hello world!')
    
    if __name__ == '__main__':
	    MyServer(host='localhost', port=80, clients=10)

**then in console**

	python test.py
	

Serve Tool
----------
Serve tool allows you to run simplest HttpServer File in one command. [dirname] will be used as base directory. 

    $ serve [dirname]
    # Will serve your current cli directory on http://127.0.0.1:8008
    

You can setup directory index file by setting up [filename], in this case [dirname] will be a [filename] directory.

 - /home/proj/
    - css
        - custom.css
    - index.html
 
To get index.html even if you go to http://127.0.0.1:8008 (and not http://127.0.0.1:8008/index.html) you must specify index.html path.

    $ serve index.html
    # In this case base directory will be */home/proj/*
    # And if you go to http://127.0.0.1:8008 server should open index.html

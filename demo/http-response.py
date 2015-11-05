#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cleave import server


class MyServer(server.BaseServer):
    """
    My HTTP Server
    """
    def client_handler(self, client):
        """
        Handles a client connection
        :param client: server.BaseClient 
        :return: None
        """
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html; charset=utf-8\n\n')

        client.send('<h1>Hello world</h1>')

        client.send('<p><strong>My Address:</strong></p>')
        client.send('<pre>{}:{}</pre>'.format(client.addr[0], client.addr[1]))

        client.send('<p><strong>Request body:</strong></p>')
        client.send('<pre>{}</pre>'.format(client.message))
        
        client.send('<hr /><small>By Cleave Server 0.13 Beta</small>')


if __name__ == '__main__':
    MyServer(port=80)
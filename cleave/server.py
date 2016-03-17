#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
from cleave.debug import Log


class BaseClient(object):
    def __init__(self, conn, addr, msg):
        self.sock = conn
        self.addr = addr
        self.message = msg
        self.buffer = []

    def flush(self):
        self.sock.send(''.join(self.buffer))
        self.close()

    def send(self, msg):
        self.buffer.append(msg)

    def close(self):
        self.sock.close()


class BaseServer(object):
    DUMP_REQUEST = False
    DUMP_RESPONSE = False
    RESTART_ON_ERROR = True
    DEFAULT_TIMEOUT = None
    AUTOFLUSH_RESPONSE = True
    CLIENT_OBJECT = BaseClient
    LOG_CLIENTS = True

    """
    Server class
    """
    def __init__(self, host='127.0.0.1', port=8008, clients=10):
        socket.setdefaulttimeout(float(self.DEFAULT_TIMEOUT) if self.DEFAULT_TIMEOUT is not None else None)
        self.clients = clients
        self.addr = (host, port)
        self.conn = None
        self.startup_handler()

    def client_handler(self, client):
        """
        Call when client was connected
        :param client: Client object
        :return: None
        """
        pass

    def client_error_handler(self, exception=None):
        """
        Calls when excepts client error
        :param exception: Exception
        :return:
        """
        pass

    def startup_handler(self):
        """
        Calls when server is starting
        :return:
        """
        self._connection(socket.AF_INET, socket.SOCK_STREAM)
        self._loop()

    def shutdown_handler(self, exception=None):
        """
        Call before server will shutting down
        :return:
        """
        if self.RESTART_ON_ERROR and exception is not None:
            self.startup_handler()

    def _connection(self, *args, **kwargs):
        """
        Creation socket
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # Create socket
            self.conn = socket.socket(*args, **kwargs)
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind address
            self.conn.bind(self.addr)

            # Listen clients
            self.conn.listen(self.clients)
        except socket.error as e:
            Log.critical(e)
            sys.exit()

    def _shutdown(self, exception=None):
        """
        Shutdown current loop
        :return:
        """
        self.conn.close()
        self.shutdown_handler(exception)

    def _loop(self):
        """
        Main loop
        :return:
        """
        if self.conn is None:
            Log.critical('Server is not initialized')
            sys.exit()

        Log.info('Server listen {}:{}'.format(self.addr[0], self.addr[1]))
        Log.debug('Waiting maximum {} clients'.format(self.clients))

        try:
            # Wait for a new clients
            while True:
                # New client accepted
                conn, addr = self.conn.accept()
                if self.LOG_CLIENTS:
                    Log.info('New client connected {}:{}'.format(addr[0], addr[1]))

                # Read message
                message = self._read(conn)

                # Dump request
                if self.DUMP_REQUEST and self.LOG_CLIENTS:
                    Log.info('Request received:\n{}\n'.format(message))

                # Handle client
                client = self.CLIENT_OBJECT(conn, addr, message)
                try:
                    self.client_handler(client)
                except Exception as e:
                    Log.warning('Client error: {}'.format(e.message))
                    self.client_error_handler(e)

                    # Dump response
                    if self.DUMP_RESPONSE:
                        Log.info('Response will send:\n{}\n'.format(''.join(client.buffer)))

                    if self.AUTOFLUSH_RESPONSE is True:
                        client.flush()
                    continue

                # Dump response
                if self.DUMP_RESPONSE:
                    Log.info('Response will send:\n{}\n'.format(''.join(client.buffer)))

                # Flush response
                if self.AUTOFLUSH_RESPONSE is True:
                    client.flush()

        except KeyboardInterrupt:
            # Shutting down server
            self._shutdown()
            Log.info('Server is down!')
            sys.exit()

        except Exception as e:
            # Shutting down server
            Log.error(e)

            # Exit or restart
            if self.RESTART_ON_ERROR is False:
                Log.warning('Server is down!')
                sys.exit()
            else:
                Log.info('Server is now restarting')

            self._shutdown(e)

    @staticmethod
    def _read(sock, chunk_len=2048):
        """
        Read all chunks from socket connection
        :param sock:
        :param chunk_len:
        :return:
        """
        result = sock.recv(chunk_len)
        if len(result) == chunk_len:
            while True:
                tmp = sock.recv(chunk_len)
                result += tmp
                if len(tmp) < chunk_len:
                    break
        return result


__all__ = ['BaseClient', 'BaseServer']

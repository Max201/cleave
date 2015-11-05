#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import datetime


class Log(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def message(msg):
        print datetime.datetime.now().strftime('[%Y-%m-%d %H:%M] ') + str(msg)

    @staticmethod
    def debug(msg):
        Log.message('[DEBUG]    ' + str(msg))

    @staticmethod
    def warning(msg):
        Log.message('[WARNING]  ' + Log.WARNING + str(msg) + Log.ENDC)

    @staticmethod
    def error(msg):
        Log.message('[ERROR]    ' + Log.FAIL + str(msg) + Log.ENDC)

    @staticmethod
    def critical(msg):
        Log.message('[CRITICAL] ' + Log.FAIL + Log.BOLD + str(msg) + Log.ENDC)


class BaseClient(object):
    def __init__(self, conn, addr, msg):
        self.sock = conn
        self.addr = addr
        self.message = msg
        self.buffer = []

    def send(self, msg):
        self.buffer.append(msg)

    def close(self):
        self.sock.close()


class BaseServer(object):
    """
    Server class
    """
    def __init__(self, host='127.0.0.1', port=8008, clients=10, client_object=BaseClient):
        self.client_object = client_object
        self.clients = clients
        self.addr = (host, port)
        self.conn = None

        self._loop()

    def client_handler(self, client):
        """
        Call when client was connected
        :param client: Client object
        :return: None
        """
        pass

    def startup_handler(self):
        """
        Calls when server is starting
        :return:
        """
        self._connection(socket.AF_INET, socket.SOCK_STREAM)

    def shutdown_handler(self):
        """
        Call before server will shutting down
        :return:
        """
        pass

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

    def _loop(self):
        """
        Main loop
        :return:
        """
        self.startup_handler()

        if self.conn is None:
            Log.critical('Server is not initialized')
            sys.exit()

        Log.warning('Server listen {}:{}'.format(self.addr[0], self.addr[1]))
        Log.debug('Waiting maximum {} clients'.format(self.clients))

        try:
            while True:
                conn, addr = self.conn.accept()
                # New client accepted
                Log.debug('New client connected {}:{}'.format(addr[0], addr[1]))
                message = self._read(conn)

                # Handle client
                client = self.client_object(conn, addr, message)
                self.client_handler(client)

                # Send response
                conn.send(''.join(client.buffer))
                conn.close()
        except KeyboardInterrupt:
            print '\b\b\b\b\b'
            self._shutdown()
            Log.warning('Server is down!')
            sys.exit()
        except Exception as e:
            Log.warning(e)
            self._shutdown()
            Log.warning('Server is down!')
            sys.exit()

    def _shutdown(self):
        """
        Shutdown current loop
        :return:
        """
        self.shutdown_handler()
        self.conn.close()

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
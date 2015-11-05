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

    def send(self, msg):
        self.sock.send(msg)

    def close(self):
        self.sock.close()


class BaseServer(object):
    """
    Server class
    """
    def __init__(self, host='127.0.0.1', port=8008, clients=10):
        self.addr = (host, port)
        self.clients = clients

        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.bind(self.addr)
            self.conn.listen(self.clients)
        except socket.error as e:
            Log.critical(e)
            sys.exit()

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
        Calls when server is running
        :return:
        """
        pass

    def shutdown_handler(self):
        """
        Call before server will shutting down
        :return:
        """
        pass

    def _loop(self):
        """
        Main loop
        :return:
        """
        Log.warning('Server listen {}:{}'.format(self.addr[0], self.addr[1]))
        Log.debug('Waiting maximum {} clients'.format(self.clients))
        self.startup_handler()

        try:
            while True:
                conn, addr = self.conn.accept()
                message = self._read(conn)
                client = BaseClient(conn, addr, message)
                self.client_handler(client)
                client.close()
        except Exception as e:
            Log.warning(e)
            self._shutdown()
            Log.warning('Server is down!')
            sys.exit()
        except KeyboardInterrupt:
            print '\b\b\b\b\b'
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
    def _read(sock, pair=1024):
        resp = tmp = sock.recv(pair)
        while len(tmp) < pair:
            tmp = sock.recv(pair)
            resp += tmp

        return resp
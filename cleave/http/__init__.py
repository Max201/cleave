#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cleave.debug import Log
from cleave.http import status
from cleave.http.request import Request
from cleave.http.response import Response
from cleave.server import BaseClient, BaseServer
from cleave.http.handler import HandleRequest


class HttpServer(BaseServer):
    LOG_CLIENTS = False
    DUMP_REQUEST = False
    DUMP_RESPONSE = False
    AUTOFLUSH_RESPONSE = False
    HTTP_REQUEST_HANDLER = HandleRequest

    @staticmethod
    def set_request_handler(handler):
        HttpServer.HTTP_REQUEST_HANDLER = handler

    def client_handler(self, client):
        """
        Handle client and trigger http_request handler
        """

        # Prepare request
        request = Request.parse(client.message)
        Log.info('Request: {}'.format(request))

        # Handle and process
        HttpServer.HTTP_REQUEST_HANDLER(
            client=client,
            request=request
        )

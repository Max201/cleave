#!/usr/bin/env python
# -*- coding: utf-8 -*-
import thread
from cleave.http.response import Response


class HandleRequest(object):
    REQUEST_CALLBACK = None

    """
    Handle request in a new thread
    """
    def __init__(self, client, request, handler=None):
        self.client = client
        self.request = request
        self._process()

    @staticmethod
    def set_request_callback(callback):
        HandleRequest.REQUEST_CALLBACK = callback

    def handler(self, client, request):
        """
        Process request and serve response
        :param client:
        :param request:
        :return:
        """
        response = Response(content='<h1>It works</h1><hr><small>Cleave serve tool v0.16</small>')
        client.send(response._compile())
        client.flush()

    def _process(self):
        """
        Threading requests
        :return:
        """
        thread.start_new_thread(
            getattr(self, str(HandleRequest.REQUEST_CALLBACK)),
            (self.client, self.request)
        )
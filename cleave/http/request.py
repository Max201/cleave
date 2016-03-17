#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Request(object):
    def __init__(self, method, headers, path, get=None, post=None, cookie=None):
        self.method = method
        self.headers = headers
        self.uri = path
        self.GET = get or {}
        self.POST = post or {}
        self.COOKIE = cookie or {}

    def __str__(self):
        return '{} {}'.format(self.method, self.uri)

    def __unicode__(self):
        return '{} {}'.format(self.method, self.uri)

    @staticmethod
    def parse(raw_request):
        headers = {}
        request_uri = '/'
        request_method = 'GET'
        request_get = {}
        request_cookie = {}

        # Parse headers
        for line in raw_request.split("\n"):
            # Stop processing headers
            if line.strip('\r\n. ') == '':
                break

            # Process first headers line
            if ':' not in line:
                data = line.split(' ')
                request_method = data[0].strip().upper()
                request_uri = data[1].strip()
                continue

            # Parse headers
            data = line.split(':')
            headers[data[0].strip().upper()] = data[1].strip()

        # Parse get parameters
        get_request = request_uri.split('?')
        if len(get_request) > 1:
            for data in get_request[1].split('&'):
                data = data.split('=')
                request_get[data[0].strip()] = None
                if len(data) > 1:
                    request_get[data[0].strip()] = data[1].strip()

        # Parse cookies
        cookies = headers.get('COOKIE') or ''
        if cookies:
            for item in cookies.split(';'):
                item = item.strip().split('=')
                request_cookie[item[0].strip()] = None
                if len(item) > 1:
                    request_cookie[item[0].strip()] = item[1].strip()

        return Request(
            method=request_method,
            path=request_uri,
            headers=headers,
            get=request_get,
            cookie=request_cookie
        )
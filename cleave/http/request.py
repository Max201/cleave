#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urlparse, parse_qs


class Request(object):
    def __init__(self, method, headers, uri, path, raw, body=None, get=None, post=None, cookie=None):
        self.method = method
        self.headers = headers
        self.raw = raw
        self.path = path
        self.uri = uri
        self.body = body or ''
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
        request_path = '/'
        request_method = 'GET'
        request_get = {}
        request_cookie = {}
        request_body = ''

        # Parse headers
        request_lines = raw_request.split("\n")
        line_stop = 0
        for i, line in enumerate(request_lines):
            # Stop processing headers
            if line.strip('\r\n. ') == '':
                line_stop = i
                break

            # Process first headers line
            if ':' not in line:
                data = line.split(' ')
                request_method = data[0].strip().upper()
                request_uri = data[1].strip()
                request_path = urlparse(request_uri).path
                continue

            # Parse headers
            data = line.split(':')
            headers[data[0].strip().upper()] = data[1].strip()

        # Parse request body
        request_body = '\n'.join(request_lines[line_stop:]).strip('\r\n ')

        # Parse post parameters
        request_post = parse_qs(request_body, keep_blank_values=True)

        # Parse get parameters
        request_get = parse_qs(urlparse(request_uri).query, keep_blank_values=True)

        # Parse cookies
        cookies = headers.get('COOKIE') or ''
        if cookies:
            for item in cookies.split(';'):
                item = item.strip().split('=')
                request_cookie[item[0].strip()] = None
                if len(item) > 1:
                    request_cookie[item[0].strip()] = item[1].strip()

        return Request(
            raw=raw_request,
            method=request_method,
            path=request_path,
            uri=request_uri,
            headers=headers,
            get=request_get,
            post=request_post,
            cookie=request_cookie,
            body=request_body
        )
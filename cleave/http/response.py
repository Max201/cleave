#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from cleave.http import status


class Cookie(object):
    def __init__(self, value, expires=None, domain=None, path=None, secure=None, http_only=None):
        self.value = value
        self.expires = expires or {}
        self.domain = domain
        self.path = path
        self.secure = secure
        self.http_only = http_only

    def _compile(self, name):
        properties = []
        properties.append('{}={}'.format(name, self.value))

        if self.path is not None:
            properties.append('path={}'.format(self.path))
        if self.domain is not None:
            properties.append('domain={}'.format(self.domain))
        if self.expires is not None:
            date = datetime.datetime.now() + datetime.timedelta(**self.expires)
            properties.append('expires={}'.format(date.strftime("%d %b %Y %H:%M:%S GMT")))
        if self.secure is not None and self.secure:
            properties.append('Secure')
        if self.http_only is not None and self.http_only:
            properties.append('HttpOnly')

        return '; '.join(properties)


class Response(object):
    def __init__(self, code=200, content='', headers=None, cookie=None):
        self.code = code
        self.content = ''
        self.headers = headers or {'Content-Type': 'text/html; charset=utf-8'}
        self.cookie = cookie or {}

        # Filtering cookies
        self.cookie = {val[0]: val[1] if isinstance(val[1], Cookie) else Cookie(val[1]) for val in self.cookie.iteritems()}

        # Set content
        self.set_content(content)

    def set_content(self, content=''):
        self.headers['Content-Length'] = len(content)
        self.content = content

    def _compile(self):
        response_lines = []

        # Compile response status
        response_lines.append('HTTP/1.1 {} {}'.format(self.code, status.msg[str(self.code)]))

        # Compile headers
        for key, val in self.headers.iteritems():
            response_lines.append('{}: {}'.format(key, val))

        # Compile cookies
        for name, cookie in self.cookie.iteritems():
            response_lines.append('Set-Cookie: {}'.format(cookie._compile(name)))

        response_lines.append('')
        response_lines.append(self.content)

        return '\r\n'.join(response_lines)
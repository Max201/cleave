#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mimetypes
from sys import argv
from cleave.http import HttpServer
from cleave.http.handler import HandleRequest
from cleave.http.response import Response
from cleave.debug import Log


class FileStorage(HandleRequest):
    BASE_DIR = None
    BASE_FILE = None

    @staticmethod
    def get_file_path(request_uri):
        request_uri = request_uri.replace('/', os.path.sep).replace('\\', os.path.sep)
        return FileStorage.BASE_DIR + request_uri

    @staticmethod
    def get_file_type(request_uri):
        return mimetypes.guess_type(request_uri)[0]

    @staticmethod
    def create_headers(request_uri):
        return {
            'Content-Type': FileStorage.get_file_type(request_uri),
            'Content-Length': os.path.getsize(FileStorage.get_file_path(request_uri))
        }

    @staticmethod
    def get_readable_size(filepath):
        size = os.path.getsize(filepath)
        sizes = {
            'TBytes': 1024 * 1024 * 1024 * 1024,
            'GBytes': 1024 * 1024 * 1024,
            'MBytes': 1024 * 1024,
            'KBytes': 1024
        }

        for name, mul in sizes.iteritems():
            if size > mul:
                return str(round(float(size) / mul, 2)) + ' ' + name

        return str(size) + ' Bytes'

    @staticmethod
    def serve_directory(filepath, uri):
        content = '<table width="100%" cellpadding="10">'
        content += '<thead style="background: #f5f5f5"><tr><td>Filename</td><td>Size</td><td>Type</td></tr></thead>'
        content += '<tbody>'

        for file in os.listdir(filepath):
            if file == '.' or file == '..':
                continue

            abspath = filepath + '/' + file
            link = uri.strip('/') + '/' + file
            size = FileStorage.get_readable_size(abspath) if os.path.exists(abspath) and not os.path.isdir(abspath) else '---'
            content += '<tr><td><a href="{}">{}</a></td><td><b>{}</b></td><td>{}</td></tr>'.format(
                link, file, size, FileStorage.get_file_type(file)
            )

        content += '</tbody>'
        content += '<tfoot style="background: #f5f5f5"><tr><td>Filename</td><td>Size</td><td>Type</td></tr></tfoot>'
        content += '</table>'
        content += '<hr><small>Powered by <a href="https://github.com/Max201/cleave" target="_blank">cleave</a> package <b>serve</b> tool</small>'
        return content


    @staticmethod
    def serve_file(client, request):
        if request.uri == '/' and FileStorage.BASE_FILE is not None:
            request.uri = FileStorage.BASE_FILE

        filepath = FileStorage.get_file_path(request.uri)

        # File not found
        if not os.path.exists(filepath):
            client.send(Response(code=404, content='<h1>Page not found</h1>')._compile())
            client.flush()
            Log.error('File not found {}'.format(filepath))
            return

        # Create response
        response = Response(code=200, headers=FileStorage.create_headers(request.uri))

        # Serve directory
        if os.path.isdir(filepath):
            response.set_content(FileStorage.serve_directory(filepath, request.uri))
            response.headers['Content-Type'] = 'text/html'
        else:
            response.set_content(file(filepath, 'rb').read())

        # Send file
        client.send(response._compile())
        client.flush()


def serve(args=None):
    arguments = args or argv
    path = os.getcwd()
    if len(arguments) > 1 and os.path.exists(os.path.abspath(arguments[1])):
        path = os.path.abspath(arguments[1])
        if not os.path.isdir(os.path.abspath(arguments[1])):
            FileStorage.BASE_FILE = os.path.basename(arguments[1])
            path = os.path.dirname(os.path.abspath(arguments[1]))

    Log.info('Selected folder: {}'.format(path))
    Log.info('Served on http://127.0.0.1:8008/')

    # Setup filestorage
    FileStorage.BASE_DIR = path
    FileStorage.set_request_callback('serve_file')

    # Setup Http server
    HttpServer.set_request_handler(FileStorage)
    HttpServer(port=8008, clients=99)
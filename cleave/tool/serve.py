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
    def format_size(size=0):
        sizes = {
            'TBytes': 1024 * 1024 * 1024 * 1024,
            'GBytes': 1024 * 1024 * 1024,
            'MBytes': 1024 * 1024,
            'KBytes': 1024,
        }

        for name, mul in sizes.iteritems():
            if size > mul:
                return str(round(float(size) / mul, 2)) + ' ' + name

        if size == 0:
            return ''

        return str(size) + ' Bytes'

    @staticmethod
    def read_and_sort_folder_files(folder):
        files = []
        dirs = []

        for item in os.listdir(folder):
            if item == '.' or item == '..':
                continue

            abspath = folder.rstrip('/') + os.path.sep + item
            if os.path.isdir(abspath):
                dirs.append({
                    'name': item,
                    'path': abspath,
                    'size': 0,
                    'dir': True
                })

                continue

            files.append({
                'name': item,
                'path': abspath,
                'size': os.path.getsize(abspath),
                'dir': False
            })

        return {
            'items': dirs + files,
            'size': sum(map(lambda x: x['size'], files)),
            'length': len(dirs) + len(files)
        }

    @staticmethod
    def serve_directory(filepath, uri):
        navigation = []
        full_path_pairs = uri.rstrip('/').split('/')
        for i, item in enumerate(full_path_pairs):
            if item == '':
                navigation.append(['/', FileStorage.BASE_DIR])
                continue
            navigation.append(['/'.join(full_path_pairs[:i+1]), item])
        navigation = '<b class="help-text"> / </b>'.join(map(lambda x: '<a href="{}">{}</a>'.format(*x), navigation))
        dir_items = FileStorage.read_and_sort_folder_files(filepath)

        content = '<!DOCTYPE html><html lang="en"><head>'
        content += '<title>Cleave: Serve[{}]</title>'.format(uri)
        content += '<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Roboto:300,400,500,700">'
        content += '<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/icon?family=Material+Icons">'
        content += '<link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">'
        content += '<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/0.5.9/css/bootstrap-material-design.min.css">'
        content += '<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/0.5.9/css/ripples.min.css">'
        content += '</head><body>'
        content += '<nav class="navbar navbar-info"><div class="text-center"><ul style="float:none;display:inline-block;" class="nav navbar-nav"><li style="font-size: 38px;">Folder served by cleave Http File Server</li></ul></div></nav>'.format(uri)
        content += '<div class="row"><div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12">'
        content += '<h5>&nbsp;&nbsp;{}</h5>'.format(navigation)
        content += '<table class="table table-striped table-hover table-bordered">'
        content += '<thead><tr><td>Filename <span class="badge badge-default">{}</span></td><td>Size <span class="badge badge-default">{}</span></td><td>Type</td></tr></thead>'.format(
            dir_items['length'], FileStorage.format_size(dir_items['size'])
        )

        content += '<tbody>'
        for file in dir_items['items']:
            link = uri.rstrip('/') + '/' + file['name']
            icon = '<span class="glyphicon glyphicon-file"></span> ' if not file['dir'] else '<span class="glyphicon glyphicon-folder-close"></span> '
            content += '<tr><td>{} <a href="{}">{}</a></td><td><b>{}</b></td><td>{}</td></tr>'.format(
                icon, link, file['name'], FileStorage.format_size(file['size']), FileStorage.get_file_type(file['name'])
            )

        content += '</tbody>'
        content += '<tfoot><tr><td>Filename <span class="badge badge-default">{}</span></td><td>Size <span class="badge badge-default">{}</span></td><td>Type</td></tr></tfoot>'.format(
            dir_items['length'], FileStorage.format_size(dir_items['size'])
        )

        content += '</table></div></div>'
        content += '<div class="text-center">Powered by <a href="https://github.com/Max201/cleave" target="_blank">cleave</a> package <b>serve</b> tool</div>'
        content += '</body></html>'
        return content


    @staticmethod
    def serve_file(client, request):
        if request.path == '/' and FileStorage.BASE_FILE is not None:
            request.path = '/' + str(FileStorage.BASE_FILE)

        filepath = FileStorage.get_file_path(request.path)

        # File not found
        if not os.path.exists(filepath):
            client.send(Response(code=404, content='<h1>Page not found</h1>')._compile())
            client.flush()
            Log.error('File not found {}'.format(filepath))
            return

        # Create response
        response = Response(code=200, headers=FileStorage.create_headers(request.path))

        # Serve directory
        if os.path.isdir(filepath):
            response.set_content(FileStorage.serve_directory(filepath, request.path))
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
        else:
            response.set_content(file(filepath, 'rb').read())

        # Send file
        client.send(response._compile())
        client.flush()


def serve(args=None):
    arguments = args or argv
    path = os.getcwd()
    srv_conf = {
        'host': '127.0.0.1',
        'port': '8008'
    }

    if len(arguments) > 1 and os.path.exists(os.path.abspath(arguments[1])):
        path = os.path.abspath(arguments[1])
        if not os.path.isdir(os.path.abspath(arguments[1])):
            FileStorage.BASE_FILE = os.path.basename(arguments[1])
            path = os.path.dirname(os.path.abspath(arguments[1]))

    if len(arguments) > 2:
        srv_data = arguments[2].strip().split(':')
        srv_host = srv_data[0] or srv_conf['host']
        srv_port = srv_conf['port']
        if len(srv_data) > 1:
            srv_port = srv_data[1]
        if srv_host == '0':
            srv_host = srv_conf['host']

        srv_conf['host'] = srv_host
        srv_conf['port'] = srv_port

    Log.debug('Selected folder: {}'.format(path))
    Log.debug('Should be available on http://{}:{}/'.format(srv_conf['host'], srv_conf['port']))

    # Setup filestorage
    FileStorage.BASE_DIR = path
    FileStorage.set_request_callback('serve_file')

    # Setup Http server
    HttpServer.set_request_handler(FileStorage)
    HttpServer(
        host=srv_conf['host'],
        port=int(srv_conf['port']),
        clients=99
    )

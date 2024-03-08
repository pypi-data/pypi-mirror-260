#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2024 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor.Man                                          #
#                                                           #
#      Version: 1.0 -                                       #
#                                                           #
#############################################################
#
#
#  @File: server.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date:  Wed Jan 24 09:59:26 CST 2024
#
import logging
import json
import os

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from . import __version__
from .handler import SystemHandler, DirectoryHandler, AppHandler, ManHandler


SERVER_OBJECTS = {}


class HttpHandler(SimpleHTTPRequestHandler):

    server_version = "Pyarmor.Man/" + __version__
    extensions_map = {
        '': 'application/octet-stream',
        '.svg': 'image/svg+xml',
        '.css': 'text/css',
        '.html': 'text/html',
        '.js': 'application/x-javascript',
        }

    def __init__(self, request, client_address, server, directory=None):
        if directory is None:
            directory = os.path.join(os.path.dirname(__file__), 'static')
        super().__init__(request, client_address, server, directory=directory)

    def do_OPTIONS(self):
        """Serve a OPTIONS request."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def dispatch(self, path, args):
        path = path[1:].strip('/') + '/'
        pname, meth = path.split('/', 1)
        for name, obj in SERVER_OBJECTS.items():
            if pname == name and hasattr(obj, 'dispatch'):
                return obj.dispatch(meth[:-1], args)

        raise RuntimeError('no handler for "%s"' % self.path)

    def do_POST(self):
        """Serve a POST request."""
        t = self.headers.get('Content-Type')
        self.log_message("Content-Type: %s", t)

        n = int(self.headers.get('Content-Length', 0))
        if n == 0:
            args = {}
        else:
            args = json.loads(self.rfile.read(n).decode())
        self.log_message("Post-Data: %s", args)

        result = dict(err=0)
        try:
            result['data'] = self.dispatch(self.path, args)
        except Exception as e:
            logging.exception('Failed to handle request')
            self.log_error("Failed to handle request: %s", str(e))
            result['err'] = 1
            result['data'] = str(e)

        data = json.dumps(result).encode()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        self.wfile.write(data)


def change_language(cfg, lang='en'):
    import gettext
    # path = os.path.join(os.path.dirname(__file__), 'locale')
    # gettext.translation('pyarmor', languages=[lang]).install(
    #     'pyarmor', path)
    gettext.NullTranslations().install()


def start_server(host, port, no_browser=False, cfg=None):
    change_language(cfg)

    server = TCPServer((host, port), HttpHandler)

    SERVER_OBJECTS['sys'] = SystemHandler(cfg)
    SERVER_OBJECTS['dir'] = DirectoryHandler(cfg)
    SERVER_OBJECTS['app'] = AppHandler(cfg)
    SERVER_OBJECTS['man'] = ManHandler(cfg)

    if not no_browser:
        from webbrowser import open_new_tab
        index = 'index.html'
        open_new_tab("http://%s:%d/%s" % (host, port, index))

    server.serve_forever()

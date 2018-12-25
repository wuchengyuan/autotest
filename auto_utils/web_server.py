#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_utils.common import *
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse

work_path = get_project_path() + 'result/'

# MIME-TYPE
content_type = {
    '.html': 'text/html',
    '.htm': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.txt': 'text/plain',
    '.log': 'text/plain',
    '.avi': 'video/x-msvideo'}


class HttpRequest(BaseHTTPRequestHandler):
    def do_GET(self):
        send_reply = False
        query_path = urlparse(self.path)
        file_path, query = query_path.path, query_path.query
        if file_path.endswith('/'):
            file_path += 'result.html'
        filename, file_ext = path.splitext(file_path)
        mime_type = content_type.get(file_ext)
        if mime_type:
            send_reply = True
        if send_reply is True:
            try:
                with open(path.realpath(work_path + file_path), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    port = 8000
    logging.info('starting server, port', port)
    server_address = ('', port)
    httpd = HTTPServer(server_address, HttpRequest)
    logging.info('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

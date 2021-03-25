import os
import sys
import mimetypes
from datetime import datetime
from os.path import getsize

sys.path.append(os.path.realpath(os.path.dirname(sys.executable) + "/../.."))
from web_server.handler.consts.http_status import (
    STATUS_DESCRIPTION,
)


class Response:
    def __init__(self, method='GET', protocol='HTTP/1.1', status=200, filepath=None):
        self.method = method
        self.status = status
        self.protocol = protocol
        self.filepath = filepath

        self.headers = {
            'Server': 'Prefork web server',
            'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Connection': 'Close',
        }
        self.body = bytes()
        
        if not self.filepath is None:
            file_size = getsize(self.filepath)
            mimetype, _ = mimetypes.guess_type(self.filepath)
            self.headers['Content-Length'] = file_size
            self.headers['Content-Type'] = mimetype

            with open(self.filepath, 'rb') as f:
                self.body = f.read()
    
    @property
    def raw_data(self):
        raw_data = '\r\n'.join([self.__status_line, self.__raw_headers, '\r\n'])
        raw_data = raw_data.encode()
        if self.method != 'HEAD':
            raw_data += self.body
        return raw_data
    
    @property
    def __status_line(self):
        status_desc = STATUS_DESCRIPTION[self.status]
        return f'{self.protocol} {self.status} {status_desc}'
    
    @property
    def __raw_headers(self):
        headers = [f'{key}: {val}' for key, val in self.headers.items()]
        raw_headers = '\r\n'.join(headers)
        return raw_headers

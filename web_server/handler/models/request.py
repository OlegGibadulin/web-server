import os
import sys
import logging
from urllib import parse

sys.path.append(os.path.realpath(os.path.dirname(sys.executable) + "/../.."))
from web_server.config import (
    DOCUMENT_ROOT,
    INDEX_FILENAME,
)

class Request:
    def __init__(self, raw_data):
        self.error = None
        self.raw_data = None
        self.method = None
        self.uri = None
        self.protocol = None
        self.filepath = None
        self.is_dir = None
        
        try:
            self.raw_data = raw_data.decode('utf-8')
            lines = self.raw_data.split('\r\n')
            
            self.method, self.uri, self.protocol = lines[0].split(' ')
            self.uri = parse.unquote(self.uri.split('?')[0])
            
            self.filepath = os.path.join(DOCUMENT_ROOT, self.uri[1:])
            self.is_dir = False
            if self.uri.endswith('/'):
                self.is_dir = os.path.isdir(self.filepath)
                self.filepath = os.path.join(self.filepath, INDEX_FILENAME)
        except Exception as e:
            # logging.error(f'Error in parsing request: {e}')
            self.error = e
    
    def __str__(self):
        return f'Method: {self.method}, URI: {self.uri}, Filepath: {self.filepath}, Error: {self.error}'

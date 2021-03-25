import os
import sys
import logging

sys.path.append(os.path.realpath(os.path.dirname(sys.executable) + "/../.."))
from web_server.handler.base import (
    BaseRequestHandler
)
from web_server.handler.models import (
    Request,
    Response,
)
from web_server.handler.consts.http_status import (
    OK_STATUS,
    BAD_REQUEST_STATUS,
    FORBIDDEN_STATUS,
    NOT_FOUND_STATUS,
    METHOD_NOT_ALLOWED_STATUS,
)


class StaticRequestHandler():
    def __init__(self):
        self.__buf_size = 1024
        self.__acceptable_methods = ['GET', 'HEAD']
        
    def handle(self, conn):
        raw_data = self.__read_request(conn)
        request = Request(raw_data)
        # logging.info(f'Accepted request: {request}')

        filepath = None
        if not request.method in self.__acceptable_methods:
            status = METHOD_NOT_ALLOWED_STATUS
        elif not request.error is None:
            status = BAD_REQUEST_STATUS
        elif request.filepath.find('../') != -1:
            status = FORBIDDEN_STATUS
        elif not os.path.exists(request.filepath):
            if request.is_dir:
                status = FORBIDDEN_STATUS
            else:
                status = NOT_FOUND_STATUS
        else:
            status = OK_STATUS
            filepath = request.filepath
        
        # logging.info(f'Response status: {status}')
        
        resp = Response(request.method, request.protocol, status, filepath)
        self.__send_response(conn, resp)

    def __read_request(self, conn):
        raw_data = b''
        while True:
            chunk = conn.recv(self.__buf_size)
            raw_data += chunk
            if len(chunk) < self.__buf_size:
                break
        return raw_data
    
    def __send_response(self, conn, resp):
        conn.sendall(resp.raw_data)

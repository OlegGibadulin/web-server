import os
import socket
import signal
import logging


class Server:
    def __init__(self, handler, host, port, max_proc=4, max_conn=255):
        self.__handler = handler
        self.__host = host
        self.__port = port
        self.__max_conn = max_conn
        self.__max_proc = max_proc
        
        self.__socket = None
        self.__workers = []
    
    def __exit__(self, exc_type, exc_value, traceback):
        for worker in self.__workers:
            os.kill(worker, signal.SIGTERM)
    
    def run(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen(self.__max_conn)
        logging.info(f'Run web server on host {self.__host}:{self.__port}')

        for _ in range(self.__max_proc):
            pid = os.fork()

            if pid != 0:
                self.__workers.append(pid)
            else:
                while True:
                    conn, addr = self.__socket.accept()
                    # logging.info(f'Accept request from {addr}')
                    self.__handler.handle(conn)
                    conn.close()
        
        for worker in self.__workers:
            os.waitpid(worker, 0)

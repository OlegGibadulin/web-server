import os
import sys
from dotenv import load_dotenv
import logging
from logging import StreamHandler, Formatter

sys.path.append(os.path.realpath(os.path.dirname(sys.executable) + "/../.."))
from web_server.server import Server
from web_server.handler import StaticRequestHandler
from web_server.config import CPU_LIMIT

load_dotenv()
SERVER_HOST = os.getenv('SERVER_HOST', default='127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', default=8000))

if __name__=='__main__':
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    static_handler = StaticRequestHandler()
    server = Server(handler=static_handler, host=SERVER_HOST, port=SERVER_PORT, max_proc=CPU_LIMIT)
    server.run()

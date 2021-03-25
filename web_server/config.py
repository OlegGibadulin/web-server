import os
import sys

CONFIG_PATH = '/etc/httpd.conf'
INDEX_FILENAME = 'index.html'

def parse_config_file(filepath=CONFIG_PATH):
    global CPU_LIMIT
    global DOCUMENT_ROOT

    with open(filepath, 'r') as f:
        for line in f:
            key, value = line.split(' ')
            if key == 'cpu_limit':
                CPU_LIMIT = int(value)
            if key == 'document_root':
                DOCUMENT_ROOT = value.rstrip('\n')

CPU_LIMIT = 4
DOCUMENT_ROOT = '/var/www/html'

parse_config_file(CONFIG_PATH)

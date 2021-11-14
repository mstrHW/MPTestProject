import os
import json
import iso8601
import logging
from imp import reload

from typing import (
    Dict,
    List,
    Optional,
    Tuple
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
EXPERIMENTS_DIR = os.path.join(ROOT_DIR, 'experiments')
COINS_DATA_V1_DIR = os.path.join(DATA_DIR, 'coins', 'v1')
COINS_DATA_V2_DIR = os.path.join(DATA_DIR, 'coins', 'v2')


CURRENCY = 'currency'
AVAILABLE = 'available'
RESERVED = 'reserved'
SIDE_BUY = 'buy'
SIDE_SELL = 'sell'


def path_join(left_path, right_path):
    return os.path.join(left_path, right_path)

def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def path_exists(directory):
    return os.path.exists(directory)

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def write_json(filename, write_message):
    with open(filename, 'w') as file:
        json.dump(write_message, file)
        logging.info('overwrite model parameters file ({})'.format(filename))


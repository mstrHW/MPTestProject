import re

from definitions import Dict
from module.data_processing.timestamp_utils import is_iso8601_format


def __is_valid_float(value):
    answer = True
    if re.match(r'^-?\d+(?:\.\d+)$', value) is None:
        answer = False
    return answer


def __validate_timestamp(timestamp):
    if not isinstance(timestamp, str):
        raise TypeError('Timestamp should be string in iso8601 format')

    if not is_iso8601_format(timestamp):
        raise ValueError('Timestamp should be string in iso8601 format')


def __validate_timeline(timeline):
    if not isinstance(timeline, list):
        raise TypeError('Timeline should be list')

    if len(timeline) == 0:
        raise ValueError('Empty timeline')

    for item in timeline:
        if not isinstance(item, dict):
            raise TypeError('Item of timeline should be a dict')

        if 'timestamp' not in item.keys():
            raise ValueError('Item has not attribute {}'.format('timestamp'))

        if ('price' not in item.keys()) and ('close' not in item.keys()):
            raise ValueError('Item has not attribute {}'.format('price'))

        __validate_timestamp(item['timestamp'])

        price_field = 'price' if 'price' in item.keys() else 'close'
        if not isinstance(item[price_field], float) and not __is_valid_float(item[price_field]):
            raise ValueError('Price value {} is not valid float'.format(item[price_field]))


def validate_data(data: Dict):
    if not isinstance(data, dict):
        raise TypeError('Wrong type')

    if len(data) == 0:
        raise ValueError('Empty data')

    for key, value in data.items():
        __validate_timeline(value)

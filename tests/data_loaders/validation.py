import pytest

from module.data_processing.validation import validate_data, __validate_timestamp, __validate_timeline


def test_wrong_dataset_type():
    with pytest.raises(TypeError):
        validate_data(list())

def test_empty_dataset():
    with pytest.raises(ValueError):
        validate_data(dict())

def test_wrong_timeline_type():
    with pytest.raises(TypeError):
        __validate_timeline(dict())

def test_empty_timeline():
    with pytest.raises(ValueError):
        __validate_timeline(list())

def test_wrong_timeline_item_type():
    with pytest.raises(TypeError):
        data = [
            1,
            2,
        ]

        __validate_timeline(data)

def test_data_without_timestamp():
    with pytest.raises(ValueError):
        data = [
            {1:1},
            {2:2},
        ]

        __validate_timeline(data)

def test_data_without_timestamp_or_price():
    with pytest.raises(ValueError):
        data = [
            {'timestamp':1},
            {'timestamp':2},
        ]
        __validate_timeline(data)

    with pytest.raises(ValueError):
        data = [
            {'price':1},
            {'price':2},
        ]
        __validate_timeline(data)


def test_wrong_timestamp_type():
    with pytest.raises(TypeError):
        __validate_timestamp(1)

def test_wrong_timestamp_format():
    with pytest.raises(ValueError):
        __validate_timestamp('123')

def test_dataset_is_valid():
    dataset = dict(ETHUSD=[
        {'timestamp': '2018-09-28T07:30:00.000Z', 'price': '230.53'},
        {'timestamp': '2018-09-28T08:00:00.000Z', 'open': '230.36', 'close': '228.28', 'min': '227.57',
         'max': '230.53', 'price': '228.28', 'volume': '1025.803', 'volumeQuote': '234618.81586'},
    ])

    validate_data(dataset)

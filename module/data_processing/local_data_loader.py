import numpy as np

from definitions import path_join, COINS_DATA_V2_DIR
from module.data_processing.timestamp_utils import from_iso, to_str


def load_local_data(symbol, start_date, end_date):
    start_date_datetime = from_iso(start_date)
    end_date_datetime = from_iso(end_date)

    file_name = '{}_{}_{}.npz'.format(symbol, to_str(start_date_datetime), to_str(end_date_datetime))
    candles_file = path_join(COINS_DATA_V2_DIR, file_name)

    candles = np.load(candles_file, allow_pickle=True)['candles'].tolist()
    market_data = {symbol: candles}

    return market_data


if __name__ == '__main__':
    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"

    dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

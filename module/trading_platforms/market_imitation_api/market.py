from definitions import List, Dict
from module.trading_platforms.market_imitation_api.input_parameters_validation import validate_fees
from module.data_processing.validation import validate_data


class Market(object):

    def __init__(self, dataset: Dict, fees: Dict = None):
        self.TIME = 0

        validate_data(dataset)
        self.timeline = dataset

        validate_fees(fees)
        self.fees = fees

    def get_max_time(self):
        return len(self.timeline[list(self.timeline.keys())[0]])

    def get_symbols_params(self):
        return self.fees

    def get_tickers(self) -> Dict[str, Dict]:
        all_symbols = list(self.timeline.keys())
        tickers_params = {}

        for symbol in all_symbols:
            if symbol in self.timeline:
                timeline = self.timeline[symbol]
            else:
                logging.message('Symbol {} was not found in timeline'.format(symbol))
                continue

            ticker = timeline[self.TIME]
            tickers_params[symbol] = ticker

        return tickers_params

    def get_candles(self, symbol: str, limit: int, period: str):
        return self.timeline[symbol][self.TIME + 1 - limit:self.TIME + 1]

    def get_timeline(self, symbol: str):
        return self.timeline[symbol][:self.TIME]

    def get_current_price(self, symbol: str) -> Dict:
        return self.timeline[symbol][self.TIME]

    def get_current_timestamp(self) -> str:
        timeline = self.timeline[list(self.timeline.keys())[0]]
        ticker = timeline[self.TIME]
        timestamp = ticker['timestamp']
        return timestamp


from module.data_processing.local_data_loader import load_local_data
if __name__ == '__main__':
    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"

    market_data = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

    market = Market(market_data)
    print(market.get_current_price('ETHUSD'))
    print(market.get_tickers())
    print(market.get_current_timestamp())

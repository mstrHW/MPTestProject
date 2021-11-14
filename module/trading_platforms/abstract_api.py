from abc import ABC, abstractmethod

from definitions import List, Dict


class AbstractApi(ABC):

    def __init__(self, api_params: Dict):
        self.api_params = api_params

    @abstractmethod
    def get_candles(self, symbol: str, limit: int = 2, period: str = 'M30') -> List[Dict]:
        return [{'timestamp': '2018-09-28T07:30:00.000Z',
                 'open': '230.91',
                 'close': '230.53',
                 'min': '229.80',
                 'max': '231.54',
                 'volume': '627.778',
                 'volumeQuote': '144858.62022'},
                {'timestamp': '2018-09-28T08:00:00.000Z', 'open': '230.36', 'close': '228.28', 'min': '227.57',
                 'max': '230.53', 'volume': '1025.803', 'volumeQuote': '234618.81586'}]


    @abstractmethod
    def get_trading_balance(self) -> Dict:
        # all currencies on balance should be returned
        return {'1ST': {'available': '0', 'reserved': '0'},
                '8BT': {'available': '0', 'reserved': '0'},
                'ABA': {'available': '0', 'reserved': '0'},
                'ABTC': {'available': '0', 'reserved': '0'}}

    @abstractmethod
    def get_trades(self, symbol: str) -> List[Dict]:
        return list()

    @abstractmethod
    def get_all_active_orders(self) -> List[Dict]:
        return list()

    @abstractmethod
    def cancel_all_orders(self) -> None:
        return None

    @abstractmethod
    def make_order(self, symbol: str, side: str, quantity: float, price: float, time_in_force: str = 'GTC') -> Dict:
        # returned message will be used like a logging record (format can be different)
        # answer with error:
        answer = {'error': {'code': 10001, 'message': 'Insufficient funds',
                            'description': 'Check that the funds are sufficient, given commissions'}}
        # answer with created order
        answer = {'id': '59653018842', 'clientOrderId': '40b4b3b5cf970dfb1c8bdf667f6cbcf8', 'symbol': 'ETHUSD', 'side': 'buy',
                  'status': 'new', 'type': 'limit', 'timeInForce': 'GTC', 'quantity': '0.050', 'price': '210.00',
                  'cumQuantity': '0.000', 'createdAt': '2018-09-30T09:29:40.557Z', 'updatedAt': '2018-09-30T09:29:40.557Z'}

        return answer


    def get_order(self, client_order_id: str, wait=None) -> Dict:
        return dict()

    def cancel_order(self, client_order_id: str) -> None:
        return None

    @abstractmethod
    def get_estimated_balance(self, tickers_params: Dict) -> float:
        # should return balance in main currency using current trading_platforms prises (bid)
        return 68.08671789952001

    @abstractmethod
    def get_symbols_params(self) -> Dict:
        # all markets should be returned (by main_currency, coin + mainCurrency format)
        return {'BTCUSD': {'min_order_size': 0.01, 'fee': 0.001, 'rebate': -0.0001, 'tick_size': 0.01},
                'DOGEUSD': {'min_order_size': 10.0, 'fee': 0.001, 'rebate': -0.0001, 'tick_size': 1e-06},
                'LTCUSD': {'min_order_size': 0.1, 'fee': 0.001, 'rebate': -0.0001, 'tick_size': 0.001},
                'XMRUSD': {'min_order_size': 0.001, 'fee': 0.001, 'rebate': -0.0001, 'tick_size': 0.01}}

    @abstractmethod
    def get_tickers_params(self) -> Dict:
        # all markets should be returned (by main_currency, coin + mainCurrency format)
        return {'BTCUSD': {'bid': 6596.96, 'ask': 6596.99, 'volume': 7844.01, 'volumeQuote': 51599275.4403},
                'DOGEUSD': {'bid': 0.00589, 'ask': 0.00592, 'volume': 107076800.0, 'volumeQuote': 630799.96379},
                'LTCUSD': {'bid': 60.782, 'ask': 60.918, 'volume': 140027.8, 'volumeQuote': 8570325.7538}}

    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        return 11.275

if __name__ == '__main__':
    print(AbstractApi.__init__.__annotations__)

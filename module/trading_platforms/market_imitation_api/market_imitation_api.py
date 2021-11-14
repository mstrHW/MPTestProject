from definitions import AVAILABLE, RESERVED, SIDE_BUY, SIDE_SELL, List, Dict, logging

from module.trading_platforms.abstract_api import AbstractApi
from module.trading_platforms.market_imitation_api.market import Market
from module.trading_platforms.market_imitation_api.player import Player
from module.data_processing.local_data_loader import load_local_data


class MarketImitationApi(AbstractApi):

    def __init__(self, main_currency: str, dataset = None, initial_player_balance: Dict = None, fees: Dict = None):
        self.main_currency = main_currency
        self.__player = Player(initial_player_balance)
        self.__market = Market(dataset, fees)

    def increase_time(self) -> None:
        self.__market.TIME += 1

    def get_max_time(self) -> int:
        return self.__market.get_max_time()

    def get_trading_balance(self) -> Dict:
        return self.__player.get_balance()

    def cancel_all_orders(self) -> None:
        return self.__player.close_orders()

    def get_symbols_params(self) -> Dict:
        return self.__market.get_symbols_params()

    def get_tickers_params(self) -> Dict:
        return self.__market.get_tickers()

    def get_estimated_balance(self) -> float:
        balances = self.get_trading_balance()

        estimated_balance = 0
        main_currency_balance = 0

        for currency, balance in balances.items():
            available = float(balance[AVAILABLE])
            reserved = float(balance[RESERVED])

            if available > 0 or reserved > 0:
                if currency == self.main_currency:
                    main_currency_balance += available
                    main_currency_balance += reserved
                else:
                    symbol = currency + self.main_currency
                    selling_price = self.get_current_price(symbol)
                    estimated_balance += available * selling_price
                    estimated_balance += reserved * selling_price

        estimated_balance += main_currency_balance

        return estimated_balance

    def get_candles(self, symbol: str, limit: int = 100, period: str = 'M30') -> List[Dict]:
        return self.__market.get_candles(symbol, limit, period)

    def get_timeline(self, symbol: str) -> List[Dict]:
        return self.__market.get_timeline(symbol)

    def make_order(self, symbol: str, side: str, quantity: float, price: float, time_in_force: str = 'GTC') -> Dict:
        main_currency = symbol[-3:]
        temp_currency = symbol[:-3]
        if (symbol[-4:] == 'USDT') or (symbol[-4:] == 'USDC'): # TODO: it's really bad
            main_currency = 'USD'
            temp_currency = symbol[:-4]
        try:
            if side == SIDE_BUY:
                self.__player.deduct_coins(main_currency, price * quantity)
                self.__player.add_coins(temp_currency, quantity)
            else:
                self.__player.deduct_coins(temp_currency, quantity)
                self.__player.add_coins(main_currency, price * quantity)

            symbol_fee = self.__market.fees[symbol]['fee']
            fee = symbol_fee * price * quantity

            timestamp = self.__market.get_current_timestamp()
            self.__player.write_trade(symbol, side, quantity, price, fee, timestamp)
            message = 'new {} order at {} was created'.format(side, symbol)
            order_params = {
                'price': price,
                'quantity': quantity,
                'message': message
            }
            logging.info(message)
        except ValueError as e:
            message = 'new {} order at {} : {}'.format(side, symbol_, e)
            order_params = {
                'error': message
            }
            logging.error(message)
        return order_params

    def get_all_active_orders(self) -> List[Dict]:
        return self.__player.active_orders

    def get_trades(self, symbol: str = None) -> List[Dict]:
        return self.__player.get_trades()

    def get_current_price(self, symbol: str) -> float:
        current_candle = self.__market.get_current_price(symbol)
        price_field = 'price' if 'price' in current_candle.keys() else 'close'
        return current_candle[price_field]


if __name__ == '__main__':
    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"
    dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

    api = MarketImitationApi('USD', dataset=dataset)
    print(MarketImitationApi.__init__.__annotations__)

    for i in range(100):
        print(i, api.get_current_price('ETHUSD'))
        api.increase_time()

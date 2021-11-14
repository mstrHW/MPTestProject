import copy

from definitions import CURRENCY, AVAILABLE, RESERVED, List, Dict
from module.trading_platforms.market_imitation_api.input_parameters_validation import validate_player_balance


class Player(object):

    def __init__(self, balance: Dict = None, trades: Dict = None):
        validate_player_balance(balance)
        self.initial_balance = balance if balance is not None else dict()
        self.balance = balance if balance is not None else dict()

        self.trades = trades if trades else list()
        self.active_orders = dict()

    def close_orders(self) -> None:
        for order in self.active_orders:
            need_to_return = order.close()
            self.balance[need_to_return[CURRENCY]] += need_to_return[QUANTITY]
        self.active_orders = dict()

    def get_trades(self) -> List[Dict]:
        return self.trades

    def get_balance(self) -> Dict:
        return copy.deepcopy(self.balance)

    def deduct_coins(self, coin: str, quantity: float) -> None:
        coin_balance = self.balance[coin][AVAILABLE]
        if (coin_balance > quantity):
            coin_balance -= quantity
            self.balance[coin][AVAILABLE] = coin_balance
        else:
            raise ValueError('not enough coins')

    def add_coins(self, coin: str, quantity: float):
        if coin not in self.balance:
            coin_balance = {}
            coin_balance[AVAILABLE] = quantity
            coin_balance[RESERVED] = 0
            self.balance[coin] = coin_balance
        else:
            self.balance[coin][AVAILABLE] += quantity

    def write_trade(self, symbol: str, side: str, quantity: float, price: float, fee: float, timestamp: str):
        symbol_trade = {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'fee': fee,
                        'timestamp': timestamp}

        self.trades.append(symbol_trade)

    def __str__(self):
        return str(self.balance)


if __name__ == '__main__':
    balance = {
        'USD': {AVAILABLE:'1000', RESERVED:'0'},
        'ETH': {AVAILABLE: '1000', RESERVED: '0'},
    }
    initial_state = PlayerState(balance)
    print(initial_state)

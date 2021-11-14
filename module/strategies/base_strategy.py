import sys

from definitions import AVAILABLE, Dict, logging
from module.trading_platforms.abstract_api import AbstractApi


class BaseStrategy(object):

    def __init__(self, api: AbstractApi, params: Dict):
        self.api = api
        self.params = params
        self.iteration = 0

    def main(self):
        price = self.api.get_current_price('ETHUSD')
        fee = self.api.get_symbols_params()['ETHUSD']['fee']

        eth_count = float(self.api.get_trading_balance()['ETH'][AVAILABLE])
        usd_count = float(self.api.get_trading_balance()['USD'][AVAILABLE])

        message = 'before rebalance: price: {}, eth_in_usd: {:.3f}, usd_count: {:.3f}'.format(price, eth_count * price, usd_count)
        logging.info(message)

        diff = eth_count * price - usd_count
        diff_quantity = abs(diff) / price / 2 / (1 - fee)

        if diff > 0:
            self.api.make_order('ETHUSD', 'sell', diff_quantity, price)
        else:
            self.api.make_order('ETHUSD', 'buy', diff_quantity, price)


        eth_count = float(self.api.get_trading_balance()['ETH'][AVAILABLE])
        usd_count = float(self.api.get_trading_balance()['USD'][AVAILABLE])

        self.iteration += 1
        message = 'after rebalance: price: {}, usd_count: {:.3f}, eth_count: {:.3f}, eth_summ_in_usd: {:.3f}'.format(price, usd_count, eth_count, eth_count * price)
        logging.info(message)

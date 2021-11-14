from definitions import List, Dict, write_json, logging
from module.trading_platforms.market_imitation_api.market_imitation_api import MarketImitationApi


class Backtesting(object):
    def __init__(self, strategy, strategy_params, dataset, market_fees, main_currency='USD', initial_player_balance=None, iterations_count=None):
        self.strategy_name = strategy.__class__.__name__
        self.strategy_params = strategy_params

        self.initial_player_balance = initial_player_balance
        self.market_fees = market_fees

        self.__api = MarketImitationApi(main_currency, dataset=dataset, initial_player_balance=initial_player_balance, fees=market_fees)
        self.__strategy = strategy(self.__api, strategy_params)

        self.__player_balance_history = [initial_player_balance]
        self.__estimated_player_balance_history = [self.__api.get_estimated_balance()]

        self.__iterations_count = iterations_count if iterations_count is not None else self.__api.get_max_time()

    def run(self):
        logging.info('Simulation started')
        for i in range(self.__iterations_count):
            message = '===== Iteration {} ====='.format(i)
            logging.info(message)
            self.__strategy.main()
            self.__player_balance_history.append(self.__api.get_trading_balance())
            self.__estimated_player_balance_history.append(self.__api.get_estimated_balance())
            self.__api.increase_time()

    def get_trades(self) -> List[Dict]:
        return self.__api.get_trades()

    def get_timeline(self, symbol: str) -> List[Dict]:
        return self.__api.get_timeline(symbol)

    def get_player_balance_history(self) -> List[Dict]:
        return self.__player_balance_history

    def get_estimated_player_balance_history(self) -> List[float]:
        return self.__estimated_player_balance_history

    def save(self, filename: str):
        description = dict()
        description['strategy'] = self.strategy_name
        description['strategy_params'] = self.strategy_params

        description['initial_player_balance'] = self.initial_player_balance
        description['market_fees'] = self.market_fees
        description['iterations_count'] = self.__iterations_count

        description['player_balance_history'] = self.__player_balance_history
        description['estimated_player_balance_history'] = self.__estimated_player_balance_history
        description['trades'] = self.get_trades()

        write_json(filename, description)

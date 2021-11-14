import matplotlib.pyplot as plt

from module.data_processing.timestamp_utils import calc_delta
from module.utils.graph import Graph
from module.utils.backtesting import Backtesting


def __prepare_prices(first_point, timeline):
    prices_x = []
    prices = []

    price_field = 'price' if 'price' in timeline[0].keys() else 'close'
    for line in timeline:
        delta = calc_delta(first_point, line['timestamp'])
        prices_x.append(delta)
        prices.append(float(line[price_field]))

    return prices_x, prices


def __prepare_trades(first_point, trades):
    prices_x = []
    prices = []

    for trade in trades:
        delta = calc_delta(first_point, trade['timestamp'])
        prices_x.append(delta)
        prices.append(float(trade['price']))

    return prices_x, prices


def plot_trades(backtest: Backtesting, symbol: str, images_dir: str = ''):
    trades = backtest.get_trades()
    timeline = backtest.get_timeline(symbol)

    first_point = timeline[0]['timestamp']
    prices_x, prices = __prepare_prices(first_point, timeline)

    buying_trades = [trade for trade in trades if trade['side'] == 'buy']
    buying_x, buying_prices = __prepare_trades(first_point, buying_trades)

    selling_trades = [trade for trade in trades if trade['side'] == 'sell']
    selling_x, selling_prices = __prepare_trades(first_point, selling_trades)


    with Graph((16, 9), 'strategy_operations', 'delta_time (minutes)', 'price', images_dir=images_dir):
        plt.plot(prices_x, prices, 'b', label='price')
        plt.plot(buying_x, buying_prices, 'go', label='buy')
        plt.plot(selling_x, selling_prices, 'ro', label='sell')


def plot_balance_changes(backtest, currency: str, images_dir: str = ''):
    balances = backtest.get_player_balance_history()

    currency_balances = [balance[currency] for balance in balances]
    currency_count = [balance['available'] for balance in currency_balances]


    with Graph((16, 9), 'balance {} changes'.format(currency), 'delta_time (minutes)', 'balance', images_dir=images_dir):
        plt.plot(currency_count, 'b', label='{} balance'.format(currency))


def plot_estimated_balance_changes(backtest, images_dir: str = ''):
    balances = backtest.get_estimated_player_balance_history()

    with Graph((16, 9), 'estimated balance changes (in USDT)', 'delta_time (minutes)', 'balance', images_dir=images_dir):
        plt.plot(balances, 'b', label='estimated balance (USDT)')

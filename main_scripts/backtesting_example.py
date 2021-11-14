from module.utils.experiment import Experiment

from module.data_processing.local_data_loader import load_local_data
from module.data_processing.validation import validate_data

from module.utils.backtesting import Backtesting
from module.strategies.base_strategy import BaseStrategy
from module.utils.base_graphs import plot_trades, plot_balance_changes, plot_estimated_balance_changes



with Experiment('Test_2') as experiment:
    iterations_count = 800

    initial_player_balance = dict(
        ETH = dict(available=1000, reserved=0),
        USD = dict(available=1000, reserved=0),
    )

    market_fees = dict(
        ETHUSD = dict(min_order_size=0.01, fee=0.003)
    )

    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"
    dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)
    validate_data(dataset)


    strategy_params = dict()
    backtest = Backtesting(BaseStrategy, strategy_params, dataset, market_fees, initial_player_balance=initial_player_balance, iterations_count=iterations_count)
    backtest.run()
    backtest.save(experiment.description_file)


    plot_trades(backtest, 'ETHUSD', experiment.images_dir)

    plot_balance_changes(backtest, 'ETH', experiment.images_dir)
    plot_balance_changes(backtest, 'USD', experiment.images_dir)

    plot_estimated_balance_changes(backtest, experiment.images_dir)

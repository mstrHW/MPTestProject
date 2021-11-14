# MP_test_project


## Project structure

```
.
├── definitions.py                              # Defines key folders, files and variables for project
├── data
├── experiments
├── tests
├── main_scripts
|   └── backtesting_example.py                  # An example of using the main parts of the library
└── module                                      # Base folder for implemented methods and models 
    ├── data_processing                         # Defines methods of data loading and validation
    |   ├── local_data_loader.py
    |   ├── timestamp_utils.py                  # Frequently used functions for working with time fields
    |   └── validation.py
    ├── strategies
    |   └── base_strategy.py
    ├── trading_platforms
    |   ├── abstract_api.py                     # Allows to implement api for different platforms
    |   ├── market_imitation_api                # Simplified market model allowing backtesting
    |   |   ├── market_imitation_api.py         # Implements AbstractApi for use in strategies
    |   |   ├── market.py                       # Determines the state of the market, time and current price values
    |   |   ├── player.py                       # Determines the state of the user, balance and performed operations
    |   |   └── input_parameters_validation.py
    |   └── uniswap_api                         # Doesn't work
    └── utils
        ├── backtesting.py                      # Sets the initial parameters for the strategy, saves actions and intermediate results
        ├── base_graphs.py                      # Several graphs for example
        ├── experiment.py                       # Class for more convenient saving of experiment results
        └── graph.py                            # Adjusts the parameters of charts, hides unnecessary operations
    

```

## Experiment structure

```
.
├── experiment_1                                # folder for first experiment
└── experiment_2                                # folder for second experiment
    ├── images
    ├── description.json                        # Contains result and parameters to reproduce the experiment
    └── log.log
```

## Data format

The downloaded data must comply with the following rules:
1. Dataset is a dictionary using a symbol code as a key (e.g. ETHUSD)
2. Values of the dictionary are historical price data for a symbol in the form of a list of elements
3. Each element is a dictionary with required timestamp and price parameters and additional parameters (volume, volumeQuote)
4. Timestamp must be in iso8601 format

Example of correct data
```python
{
    ETHUSDT: [
    {'timestamp': '2018-09-28T07:30:00.000Z', 'price': '230.53'},
    {'timestamp': '2018-09-28T07:35:00.000Z', 'price': '232.31'},
],
    BTCUSDT: [
    {'timestamp': '2018-09-28T07:30:00.000Z', 'price': '230.53'},
    {'timestamp': '2018-09-28T07:35:00.000Z', 'price': '230.53'},
],
}

{
    ETHUSDT: [{
        'timestamp': '2018-09-28T08:00:00.000Z', 'open': '230.36', 'close': '228.28',
        'min': '227.57', 'max': '230.53', 'price': '228.28',
        'volume': '1025.803', 'volumeQuote': '234618.81586',
    }]
}
```

To check whether the data format is correct you can use the validate_data function (module.data_loaders.data_validation)

```python
from module.data_processing.local_data_loader import load_local_data
from module.data_processing.validation import validate_data

start_time = "2017-01-01T12:00:00Z"
end_time = "2018-12-01T12:00:00Z"
dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

validate_data(dataset)
```

## Trading platforms (module.trading_platforms)

When implementing strategies, it is recommended to use the API provided by this module.

1. AbstractApi - a class that defines market functions, used when developing strategies.
Ensures that inherited classes will implement all required functionality. 
Helps to implement Api for the required platform. Contains examples of function return values.
2. MarketImitationApi - used for backtesting. Simulates market behavior (with some number of assumptions) and implements AbstractApi functions
    #### Usage
    
    ```python
    from module.data_processing.local_data_loader import load_local_data
    from module.data_processing.validation import validate_data
    from module.trading_platforms.market_imitation_api.market_imitation_api import MarketImitationApi
    
    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"
    dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)
    
    initial_player_balance = dict(
        ETH=dict(available=1000, received=0),
        USD=dict(available=1000, received=0),
    )
    
    market_fees = dict(
        ETHUSD=dict(min_order_size=0.01, fee=0.003)
    )
    
    api = MarketImitationApi('USD', dataset=dataset, initial_player_balance=initial_player_balance, fees=market_fees)
    
    ```
3. UniswapApi - used to run strategies on the uniswap platform (not implemented)

## Strategies (module.strategies)

Strategies are not a separate class. For the framework it is only necessary for the strategy to accept AbstractApi as an input parameter and use its functions.
This allows, after testing the strategy, to immediately launch it on the required platform.
For backtesting the logic of strategy must be executed in the main function.

#### Usage

```python
from module.data_processing.local_data_loader import load_local_data
from module.data_processing.validation import validate_data
from module.trading_platforms.market_imitation_api.market_imitation_api import MarketImitationApi
from module.strategies.base_strategy import BaseStrategy

start_time = "2017-01-01T12:00:00Z"
end_time = "2018-12-01T12:00:00Z"
dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

validate_data(dataset)
api = MarketImitationApi('USD', dataset=dataset)

strategy_params = dict()
strategy = BaseStrategy(api, strategy_params)

for time in range(1000):
    strategy.main()
    api.increase_time()

```

## Backtesting (module.utils.backtesting)

Used to hide the logic of the MarketImitationApi, sets the initial parameters for the strategy, and also saves actions and intermediate results

#### Usage

```python
strategy_params = dict()
backtest = Backtesting(BaseStrategy, strategy_params, dataset, market_fees, initial_player_balance=initial_player_balance)
backtest.run()
backtest.save(experiment.description_file)
```

## Graph (module.utils.graph)

Adjusts the parameters of charts, hides unnecessary operations

#### Usage

```python
from module.utils.graph import Graph

with Graph((16, 9), 'Example', 'x', 'y'):
    plt.plot([1, 2, 3], label='y = x')
    plt.plot([1, 4, 9], label='y = x**2')
```

## Experiment (module.utils.experiment)

Creates several folders for an experiment, stores strategy parameters, initial parameters and charts

#### Usage

```python
with Experiment('Example') as experiment:
    experiment.images_dir
    print(experiment)
```

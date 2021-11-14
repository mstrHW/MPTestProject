import pytest

from module.trading_platforms.market_imitation_api.market_imitation_api import MarketImitationApi
from module.data_processing.local_data_loader import load_local_data


@pytest.fixture()
def resource():
    print("setup")
    initial_player_balance = dict(
        ETH=dict(available=1000, reserved=0),
        USD=dict(available=1000, reserved=0),
    )

    market_fees = dict(
        ETHUSD=dict(min_order_size=0.01, fee=0.003)
    )

    start_time = "2017-01-01T12:00:00Z"
    end_time = "2018-12-01T12:00:00Z"
    dataset = load_local_data('ETHUSD', start_date=start_time, end_date=end_time)

    api = MarketImitationApi('USD', dataset=dataset, initial_player_balance=initial_player_balance, fees=market_fees)

    yield api
    print("teardown")


class Test_MarketImitationApi:
    def test_get_current_price(self, resource):
        assert resource.get_current_price('ETHUSD') == 8.25

    def test_max_time_equals_len_of_dataset(self, resource):
        assert resource.get_max_time() == 199643

    def test_estimated_balance_at_point_zero(self, resource):
        estimated_balance = resource.get_current_price('ETHUSD') * resource.get_trading_balance()['ETH']['available']\
                            + resource.get_trading_balance()['USD']['available']
        assert resource.get_estimated_balance() == estimated_balance
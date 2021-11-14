from uniswap import Uniswap

from definitions import *
from module.trading_platforms.abstract_api import AbstractApi


eth = "0x0000000000000000000000000000000000000000"
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


class UniswapApi(AbstractApi):

    def __init__(self, api_params: Dict):
        self.api_params = api_params
        uniswap = Uniswap(**api_params)

        self.uniswap = uniswap
        self.fee = self.uniswap.get_fee_taker()

    def get_trading_balance(self) -> List[Dict]:
        eth_balance = dict(
            currency='ETH',
            available=self.uniswap.get_eth_balance(),
            reserved=0,
        )
        return [eth_balance]

    def cancel_all_orders(self) -> None:
        return None

    def get_symbols_params(self) -> Dict:
        return dict()

    def get_tickers_params(self) -> Dict:
        return dict()

    def get_estimated_balance(self, tickers_params: Dict) -> float:
        ballances = self.get_trading_balance()

        estimated_ballance = 0
        main_currency_ballance = 0

        estimated_ballance += main_currency_ballance

        return estimated_ballance

    def get_candles(self, symbol_code: str, limit: int = 100, period: str = 'M30') -> List[Dict]:
        last_price = api.uniswap.get_exchange_rate(dai)
        answer = [{'timestamp': '2018-09-28T07:30:00.000Z',
         'open': last_price,
         'close': last_price,
         'min': last_price,
         'max': last_price,
         'volume': '627.778',
         'volumeQuote': '144858.62022'}]

        return answer

    def make_order(self, side: str, quantity: float) -> Dict:
        if side == 'buy':
            self.uniswap.make_trade(eth, dai, quantity)
        else:
            self.uniswap.make_trade_output(eth, dai, quantity)

        price = self.get_candles()[0]

        return dict(symbol='ETHUSD', side=side, quantity=quantity, price=price)

    def get_all_active_orders(self) -> None:
        return None

    def get_trades(self, symbol_code: str) -> None:
        return None

    def get_current_price(self, symbol: str) -> float:
        return None


if __name__ == '__main__':
    api_params = dict(
        address=eth,
        private_key=None,
        provider='https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
        version=1,
    )
    api = UniswapApi(api_params)
    print(UniswapApi.__init__.__annotations__)
    api.get_candles('ETHUSD')

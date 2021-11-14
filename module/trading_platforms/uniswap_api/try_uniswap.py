from uniswap import Uniswap

eth = "0x0000000000000000000000000000000000000000"
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


# address = "YOUR ADDRESS"  # or None if you're not going to make transactions
# private_key = "YOUR PRIVATE KEY"  # or None if you're not going to make transactions
# version = 3  # specify which version of Uniswap to use
# provider = "WEB3 PROVIDER URL"  # can also be set through the environment variable `PROVIDER`
# uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)
# from web3 import Web3
# w3 = Web3()
provider = 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'
uniswap = Uniswap(address='0xB8C25C9eB9374f8704880aeD79c25416456dAB9A', private_key=None, version=2, provider=provider)
eth_balance = uniswap.get_eth_balance()
print(eth_balance, eth_balance / 1e18)


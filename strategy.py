# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
import logging

logger = logging.getLogger()

class GridTrading:
    def __init__(self, api: BinanceTestnetApi):
        self._api = api
        print("Hello from GridTrading")

    def create(self, params: dict):
        print("Grid created")
        for param in params:
            print(str(param) + str(params[param]))
        contract = self._api.get_contract(params['contract'])
        mark_price = self._api.get_mark_price(contract)
        print("contract is: " + str(mark_price.symbol))
        print("mark price is: " + str(mark_price.mark_price))
        self._api.place_order(contract, "BUY", 0.01, "LIMIT", 1000, "GTC")
        self._api.cancel_all_open_orders(contract)

# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
from models import *
import logging

logger = logging.getLogger()

class GridTrading:
    def __init__(self, api: BinanceTestnetApi):
        self._api = api
        print("Hello from GridTrading")
    # Create strategy
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
        self._api.place_order(contract, "BUY", 0.01, "MARKET")
        self._api.close_position(contract)
    # Process an order update from websocket
    def process_order_update(self,order_update: OrderUpdate):
        print("order update")
        print(order_update.symbol + " " + order_update.status + " " + order_update.type)
    # Process a position update from websocket
    def process_position_update(self, position_update: PositionUpdate):
        print("position update")
        print(position_update.symbol + " " + str(position_update.amount) + " " + str(position_update.accumulated_realized))
    # Process a position update from websocket
    def process_balance_update(self, balance_update: BalanceUpdate):
        print("balance update")
        print(balance_update.asset + " " + str(balance_update.wallet_balance))
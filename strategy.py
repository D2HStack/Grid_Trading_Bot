# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
from models import *
import logging

logger = logging.getLogger()

class GridTrading:
    def __init__(self, api: BinanceTestnetApi):
        self._api = api
        self._symbol = None
        self._lower_price = None
        self._upper_price= None
        self._grids = None
        self._initial_margin = None
        self._open_orders = []

    # Create strategy
    def create(self, params: dict):
        all_contracts = self._api.get_all_contracts()
        self._symbol = params['contract']
        if self._symbol in all_contracts:
            self._contract = self._api.get_contract(params['contract'])
            self._lower_price = float(params['lower_price'])
            self._upper_price = float(params['upper_price'])
            self._api.cancel_all_open_orders(self._contract)
            self._api.close_position(self._contract)
            if self._api.check_price(self._contract, self._lower_price) and self._api.check_price(self._contract, self._upper_price) and self._upper_price > self._lower_price:
                self._grids = int(params['grids'])
                if self._grids >= 2 and self._grids <= 200:
                    tick = (self._upper_price - self._lower_price) / (self._grids - 1)
                    mark_price = self._api.get_mark_price(self._contract).mark_price
                    if params['initial_margin'] is not None and params['initial_margin']:
                        self._initial_margin = float(params['initial_margin'])
                        quantity = self._initial_margin / self._grids /mark_price
                        price = self._lower_price
                        print("mark_price" + str(mark_price))
                        print("tick" + str(tick))
                        print("quantity" + str(quantity))
                        for i in range(self._grids):
                            if mark_price > price:
                                side = "BUY"
                            else:
                                side = "SELL"
                            print ("price" + str(price))
                            self._api.place_order(self._contract, side, quantity, 'LIMIT', price, "GTC")
                            price += tick
                        return "Grid on {} between {} and {} with {} grids and an initial margin {} has been created.".format(
                                self._symbol,
                                self._lower_price,
                                self._upper_price, self._grids,
                                self._initial_margin)
                    else:
                        return "The initial margin is invalid"
                else:
                    return "The number of grids shoudl be between 2 and 200"
            else:
                return "Lower price and/or Upper price is invalid"
        else:
            return "There is no contract " + str(params['contract'])

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
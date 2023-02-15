# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
from models import *
import typing
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
        self._active = False
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
                            #order = self._api.place_order(self._contract, side, quantity, 'LIMIT', price, "GTC")
                            #self._open_orders.append(order)
                            price += tick
                        self._active = True
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

    # Close a strategy
    def close(self):
        # Close position and cancel all open orders on contract
        self._api.cancel_all_open_orders(self._contract)
        self._api.close_position(self._contract)
        return 'Grid has been closed'

    # Process an order update from websocket
    def process_order_update(self, order_update: OrderUpdate):
        print("order update" + order_update.symbol + " " + order_update.status + " " + order_update.type + " " + str(order_update.price))
        if order_update.status == 'NEW':
            self._open_orders.append(order_update)
        if order_update.status == 'CANCELED':
            self._remove_order_update(order_update, self._open_orders)


    # Process a position update from websocket
    def process_position_update(self, position_update: PositionUpdate):
        print("position update")
        print(position_update.symbol + " " + str(position_update.amount) + " " + str(position_update.accumulated_realized))
    # Process a position update from websocket
    def process_balance_update(self, balance_update: BalanceUpdate):
        print("balance update")
        print(balance_update.asset + " " + str(balance_update.wallet_balance))

    # Get variables and parameters
    def get_active(self):
        return self._active
    def get_contract(self):
        return self._contract
    def get_grids(self):
        return self._grids
    def get_open_orders(self):
        sorted_open_orders = sorted(self._open_orders, key=lambda o:o.price)
        return sorted_open_orders

    ########################  ORDERS FUNCTIONS  ############################################
    # Remove an order update from a list of order updates by order_id
    def _remove_order_update(self, order_update: OrderUpdate, order_updates: typing.List[OrderUpdate]):
        for order in order_updates:
            if order.order_id == order_update.order_id:
                order_updates.remove(order)
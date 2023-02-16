# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
from models import *
import typing
import logging

logger = logging.getLogger()

class GridTrading:
    def __init__(self, api: BinanceTestnetApi):
        self._params = GridParam({'symbol': '', 'lower_price': 0, 'upper_price': 0, 'grids': 0, 'initial_margin': 0})
        self._api = api
        self._contract = None
        #self._symbol = None
        #self._lower_price = None
        #self._upper_price= None
        #self._grids = None
        #self._initial_margin = None
        self._active = False
        self._open_orders = []

    # Create strategy
    def create(self, params: GridParam):
        if self._check_params(params)['response']:
            self._contract = self._api.get_contract(params.symbol)
            self._api.cancel_all_open_orders(self._contract)
            self._api.close_position(self._contract)
            tick = (params.upper_price - params.lower_price) / (params.grids - 1)
            mark_price = self._api.get_mark_price(self._contract).mark_price
            quantity = params.initial_margin / params.grids /mark_price
            price = params.lower_price
            for i in range(params.grids):
                if mark_price > price:
                    side = "BUY"
                else:
                    side = "SELL"
                print("price" + str(price))
                self._api.place_order(self._contract, side, quantity, 'LIMIT', price, "GTC")
                #order = self._api.place_order(self._contract, side, quantity, 'LIMIT', price, "GTC")
                #self._open_orders.append(order)
                price += tick
            self._active = True
            return {'msg': "Grid on {} between {} and {} with {} grids and an initial margin {} has been created.".format(
                    params.symbol,
                    params.lower_price,
                    params.upper_price, params.grids,
                    params.initial_margin), 'response': True, 'data': params}
        else:
            return {'msg': self._check_params(params)['msg'], 'response': False, 'data': params}


    # Close a strategy
    def close(self):
        # Close position and cancel all open orders on contract
        self._api.cancel_all_open_orders(self._contract)
        self._api.close_position(self._contract)
        return 'Grid has been closed'

    # Process an order update from websocket
    def process_order(self, order: Order):
        print("order update" + order.symbol + " " + order.status + " " + order.type + " " + str(order.price))
        if order.status == 'NEW':
            self._open_orders.append(order)
        if order.status == 'CANCELED':
            self._remove_order(order, self._open_orders)

    # Process a position update from websocket
    def process_position(self, position: Position):
        print("position update")
        print(position.symbol + " " + str(position.amount) + " " + str(position.accumulated_realized))
    # Process a position update from websocket
    def process_balance_update(self, balance_update: BalanceUpdate):
        print("balance update")
        print(balance_update.asset + " " + str(balance_update.wallet_balance))


    ########################  ORDERS FUNCTIONS  ############################################
    # Remove an order update from a list of order updates by order_id
    def _remove_order(self, order: Order, orders: typing.List[Order]):
        for order in orders:
            if order.order_id == order.order_id:
                orders.remove(order)

    ########################  UTILITY FUNCTIONS  ############################################
    # Check if params are valid
    def _check_params(self, params: GridParam):
        # Check if params is valid
        if params is not None and params:
            # Check if contract exists
            all_contracts = self._api.get_all_contracts()
            if params.symbol is not None and params.symbol and params.symbol in all_contracts:
                contract = self._api.get_contract(params.symbol)
                if self._api.check_price(contract, params.lower_price) and  self._api.check_price(contract, params.upper_price):
                    if params.lower_price < params.upper_price:
                        if params.grids > 1 and params.grids < 101:
                            available = self._api.available(contract)['available']
                            if params.initial_margin <= available:
                                mark_price = self._api.get_mark_price(contract).mark_price
                                quantity = params.initial_margin / params.grids / mark_price
                                if self._api.check_quantity(contract, quantity):
                                    return {'msg': "Parameters are all valid".format(
                                        params.initial_margin), 'response': True,
                                        'data': params}
                                else:
                                    return {'msg': "Initial margin {} is not sufficient".format(
                                        params.initial_margin), 'response': False,
                                        'data': params}
                            else:
                                return {'msg': "Initial margin {} should be lower than available {}".format(
                                params.initial_margin, available), 'response': False,
                                'data': params}
                        else:
                            return {'msg': "The number of grids {} should be between 2 and 100".format(
                                params.grids), 'response': False,
                                'data': params}
                    else:
                        return {'msg': "Lower price {} should be lower than upper price {}".format(
                        params.lower_price, params.upper_price), 'response': False,
                            'data': params}
                else:
                    return {'msg': "Lower price {} and/or upper price {} are not valid prices".format(params.lower_price, params.upper_price), 'response': False,
                            'data': params}
            else:
                return {'msg': "Contract {} does not exists".format(params.symbol), 'response': False, 'data': params}
        else:
            return {'msg': "Please enter parameters for the Grid", 'response': False, 'data': params}

    # Get variables and parameters
    def get_active(self):
        return self._active
    def get_params(self):
        return self._params
    def get_open_orders(self):
        return self._open_orders


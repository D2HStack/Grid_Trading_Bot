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
        self._active = False
        self._tick = 0
        self._new_orders = []
        self._order_updates = []
        self._open_orders = []
        self._filled_orders = []
        self._matched_orders = []
        self._unmatched_orders = []
        self._unrealized_profit = 0
        self._realized_profit = 0

    # Create strategy
    def create(self, params: GridParam):
        if self._check_params(params)['response']:
            self._params = params
            self._contract = self._api.get_contract(params.symbol)
            self._api.cancel_all_open_orders(self._contract)
            self._api.close_position(self._contract)
            self._tick = (params.upper_price - params.lower_price) / (params.grids - 1)
            mark_price = self._api.get_mark_price(self._contract).mark_price
            quantity = params.initial_margin / params.grids /mark_price
            price = params.lower_price
            for i in range(params.grids):
                if mark_price > price:
                    side = "BUY"
                else:
                    side = "SELL"
                new_order = self._api.place_order(self._contract, side, quantity, 'LIMIT', price, "GTC")
                self._new_orders.append(new_order)
                price += self._tick
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
        self._active = False
        return 'Grid has been closed'

    # Process an order update from websocket
    def process_order(self, order_update: Order):
        print("order update " + order_update.symbol + " " + order_update.status + " " + order_update.side + " " + order_update.type + " " + str(order_update.price))
        if self._is_grid_order(order_update):
            self._order_updates.append(order_update)
            if order_update.status == 'NEW':
                # We don't check if it is an order from the grid
                self._open_orders.append(order_update)
                return {'msg': "A new order was added", 'processed': True, 'data': order_update}
            if order_update.status == 'CANCELED':
                result_remove_order = self._remove_order(order_update, self._open_orders)
            # Beware that partially filled orders are not processed
            if order_update.status == 'FILLED':
                #print("Filled from order update")
                result_remove_order = self._remove_order(order_update, self._open_orders)
                print(result_remove_order['msg'])
                self._filled_orders.append(order_update)
                opposite_order = self._opposite_order(order_update)
                print(opposite_order['msg'])
                replace_order = self._replace_order(order_update, opposite_order['result']['opposite_side'], opposite_order['result']['opposite_price'], opposite_order['result']['opposite_quantity'])
                print(replace_order['msg'])
                matched_order = self._match_order(order_update, opposite_order['result']['matched_order_index'])
                print(matched_order['msg'])

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
    def _remove_order(self, order_update: Order, orders: typing.List[Order]):
        for index,order in enumerate(orders):
            if order.order_id == order_update.order_id:
                removed_order = orders.pop(index)
                return {'msg': 'Order was removed', 'result': True, 'data': order}
        return {'msg': 'Order was not in the list', 'result': False, 'data': order}

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
    def get_params(self) -> GridParam:
        return self._params
    def get_value(self, name: str):
        if name == 'open_orders':
            return self._open_orders
        if name == 'filled_orders':
            return self._filled_orders
        if name == 'order_updates':
            return self._order_updates
        if name == 'unmatched_orders':
            return self._unmatched_orders
        if name == 'matched_orders':
            return self._matched_orders
        # Unrealized profit is the difference between all unmatched orders and mark price
        if name == 'unrealized_profit':
            if self._contract is not None:
                mark_price = self._api.get_mark_price(self._contract).mark_price
                unrealized_profit = 0
                for unmatched_order in self._unmatched_orders:
                    if unmatched_order.side == "BUY":
                        unrealized_profit += (mark_price - unmatched_order.price) * unmatched_order.quantity
                    elif unmatched_order.side == "SELL":
                        unrealized_profit += (unmatched_order.price - mark_price) * unmatched_order.quantity
                self._unrealized_profit = unrealized_profit
                return unrealized_profit
            else:
                return 0

        # Size of unmatched orders
        if name == 'current_margin':
            if self._contract is not None:
                mark_price = self._api.get_mark_price(self._contract).mark_price
                current_margin = 0
                for unmatched_order in self._unmatched_orders:
                    current_margin += unmatched_order.quantity * mark_price
                return current_margin
            else:
                return 0

        # Realized profit is the sum of
        if name == 'realized_profit':
            if self._matched_orders:
                realized_profit = 0
                for matched_order in self._matched_orders:
                    realized_profit += matched_order['realized_profit']
                self._realized_profit = realized_profit
                return realized_profit
            else:
                return 0

        # Total profit
        if name == 'total_profit':
            return self._unrealized_profit + self._realized_profit

        # Entry price is the average price at the time of the trade
        if name == 'entry_price':
            if self._contract is not None and self._unmatched_orders:
                sum_weighted_prices = 0
                sum_quantity = 0
                for unmatched_order in self._unmatched_orders:
                    sum_weighted_prices += unmatched_order.quantity * unmatched_order.price
                    sum_quantity += unmatched_order.quantity
                return sum_weighted_prices / sum_quantity
            else:
                return 0

        # Mark price
        if name == "mark_price":
            if self._contract is not None:
                return self._api.get_mark_price(self._contract).mark_price
            else:
                return 0


    # Check if order is an order from the grid
    def _is_grid_order(self,order):
        for new_order in self._new_orders:
            if new_order.order_id == new_order.order_id:
                return True
        return False

    # Return the opposite order, the order to cancel and matched order details or None
    def _opposite_order(self, order: Order) -> dict:
        msg = ""
        result = {'matched_order_index': None, 'opposite_side': None, 'opposite_price': None, 'opposite_quantity': None}
        opposite_side = None
        opposite_price = None
        if order.side == 'BUY':
            opposite_side = "SELL"
            opposite_price = self._api.round_price(self._contract, order.price + self._tick)
        elif order.side == 'SELL':
            opposite_side = "BUY"
            opposite_price = self._api.round_price(self._contract, order.price - self._tick)
        if opposite_price >= self._params.lower_price and opposite_price <= self._params.upper_price:
            # Search for an order to match
            for index,unmatched_order in enumerate(self._unmatched_orders):
                if self._api.are_prices_equal(self._contract, unmatched_order.price, opposite_price) and unmatched_order.side == opposite_side:
                    result['matched_order_index'] = index
                    msg = msg + "The filled order matches an unmatched order."
            # Check if there already is an open order at opposite price
            new_opposite_order = True
            for open_order in (self._open_orders):
                if self._api.are_prices_equal(self._contract, open_order.price, opposite_price) and open_order.side == opposite_side:
                    new_opposite_order = False
            if  new_opposite_order:
                msg = msg + " A new order has to be placed with side {}, price {} and quantity {}.".format(opposite_side, opposite_price, order.quantity)
                result['opposite_side'] = opposite_side
                result['opposite_price'] = opposite_price
                result['opposite_quantity'] = order.quantity
            else:
                msg = msg + " No new order to be placed because there already is an order."
        else:
            msg = msg + " No new order to be placed because price is out of range."
        return {'msg': msg, 'result': result, 'data': order}

    # Replace order
    def _replace_order(self, filled_order: Order, opposite_side: str, opposite_price: float, opposite_quantity: float) -> Order:
        if opposite_side is not None and opposite_price is not None:
            new_order = self._api.place_order(self._contract, opposite_side, opposite_quantity, 'LIMIT', opposite_price, "GTC")
            return {"msg": "A new order has been placed with price {} side {} and quantity {}".format(new_order.price, new_order.side, new_order.quantity), 'result': new_order, 'data': filled_order}
        else:
            return {"msg": "No new order has been placed", 'result': None, 'data': filled_order}

    # Build matched orders
    def _match_order(self, filled_order: Order, index: int):
        if index is not None:
            unmatched_order = self._unmatched_orders.pop(index)
            if unmatched_order.side == "BUY":
                profit = (filled_order.price *  filled_order.quantity - unmatched_order.price * unmatched_order.quantity)
                result = {"BUY": unmatched_order, "SELL": filled_order, "realized_profit": profit}
            else:
                profit = (unmatched_order.price * unmatched_order.quantity - filled_order.price * filled_order.quantity)
                result = {"BUY": filled_order, "SELL": unmatched_order, "realized_profit": profit}
            self._matched_orders.append(result)
            return {'msg': "Matched orders has generated a profit of {}".format(result['realized_profit']), 'result': result, 'data': filled_order}
        else:
            self._unmatched_orders.append(filled_order)
            return {'msg': "New unmatched order", 'result': filled_order, 'data': filled_order}
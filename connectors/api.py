# API
# All functions accessible through the API
import hashlib
import requests
import time
import typing
import hmac
from urllib.parse import urlencode
from models import *
from constants import *
import logging


logger = logging.getLogger()

class BinanceTestnetApi:
    def __init__(self):
        self._HEADERS = {'X-MBX-APIKEY': PUBLIC_KEY}

    ##############  MARKET DATA  ########################

    # Get parameters of all contracts traded Market Data Endpoints / Exchange Information
    def get_all_contracts(self) -> typing.Dict[str, Contract]:
        exchange_info = self._make_request("GET", "/fapi/v1/exchangeInfo", dict())
        contracts = dict()
        if exchange_info is not None:
            for contract in exchange_info['symbols']:
                contracts[contract['symbol']] = Contract(contract)
        return contracts

    # Get parameters of all contracts traded Market Data Endpoints / Exchange Information
    def get_contract(self, symbol: str) -> Contract:
        all_contracts = self.get_all_contracts()
        if all_contracts is not None and all_contracts:
            contract = all_contracts[symbol]
            if contract is not None and contract:
                return contract
            else:
                logger.warning("There is no contract with symbol: " + symbol)
                return None
        else:
            logger.error("No contract was found")

    # Get mark price for a contract
    def get_mark_price(self, contract: Contract) -> MarkPrice:
        data = dict()
        result = dict()
        data['symbol'] = contract.symbol
        response = self._make_request("GET", "/fapi/v1/premiumIndex", data)
        if response is not None and response:
            result = MarkPrice(response)
            result.update_time = (time.time() * 1000)
        else:
            result = None
            logger.warning("There is no mark price for contract with symbol: " + contract.symbol)
        return result

    ##############  USER DATA  ########################
    # Get balances of all contracts of a user
    def get_balances(self) -> typing.Dict[str, Balance]:
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        response = self._make_request("GET", "/fapi/v1/account", data)
        result = dict()
        if response is not None:
            for asset in response['assets']:
                result[asset['asset']] = Balance(asset)
        else:
            return None
        return result

    # Available amount
    def available(self, contract: Contract) -> dict:
        return {'asset': contract.quote_asset,
                'available': self.get_balances()[contract.quote_asset].max_withdraw_amount}

    # Get the order status based on order ID number. Account/Trades Endpoints/Query Order (USER_DATA)
    def get_order_status(self, contract: Contract, order_id: int) -> Order:
        data = dict()
        data['symbol'] = contract.symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        response = self._make_request("GET", "/fapi/v1/order", data)
        response['category'] = 'status'
        if response is not None and response:
            order_time = response['time']
            update_time = response['updateTime']
            result = Order(response)
            result.order_time = order_time
            result.update_time = update_time
        else:
            return None
        return result

    # Get all the open orders for a contract Account/Trades Endpoints/Current Open Order (USER_DATA)
    def get_open_orders(self, contract: Contract) -> typing.List[Order]:
        data = dict()
        data['symbol'] = contract.symbol
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        responses = self._make_request("GET", "/fapi/v1/openOrders", data)
        if responses is not None and responses:
            result = []
            for i in range(0, len(responses)):
                responses[i]['category'] = 'status'
                result.append(Order(responses[i]))
        else:
            return None
        return result

    # Get all positions. Account/Trades Endpoints/Position Information (USER_DATA)
    def get_positions(self) -> typing.Dict[str, Position]:
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        responses = self._make_request("GET", "/fapi/v1/positionRisk", data)
        result = dict()
        if responses is not None and responses:
            for response in responses:
                response['category'] = 'status'
                result[response['symbol']] = Position(response)
        return result

    ##############  ORDER MANAGEMENT  ########################
    # Place an order. Account/Trades Endpoints/New Order (TRADE)
    def place_order(self, contract: Contract, side: str, quantity: float, order_type: str, price=None,
                    tif=None) -> Order:
        data = dict()
        data['symbol'] = contract.symbol
        data['side'] = side
        data['type'] = order_type
        result = dict()
        if self.check_quantity(contract, quantity):
            data['quantity'] = self.round_quantity(contract, quantity)
        else:
            return None
        if self.check_price(contract, price):
            data['price'] = self.round_price(contract, price)
        if tif is not None:
            data['timeInForce'] = tif
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        response = self._make_request("POST", "/fapi/v1/order", data)
        response['category'] = 'status'
        if response is not None and response:
            order_time = data['timestamp']
            update_time = response['updateTime']
            result = Order(response)
            result.order_time = order_time
            result.update_time = update_time
        else:
            return None
        return result

    # Cancel an order. Account/Trades Endpoints/Cancel Order (TRADE)
    def cancel_order(self, contract: Contract, order_id: int) -> Order:
        data = dict()
        data['symbol'] = contract.symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        response = self._make_request("DELETE", "/fapi/v1/order", data)
        response['category'] = 'status'
        if response is not None:
            order_time = data['timestamp']
            update_time = order_time
            result = Order(response)
            result.order_time = order_time
            result.update_time = update_time
        return result

    # Cancel all open orders for a contract
    def cancel_all_open_orders(self, contract: Contract) -> typing.List[Order]:
        canceled_open_orders = []
        clear = False
        open_orders = self.get_open_orders(contract)
        if open_orders is not None and open_orders:
            for open_order in open_orders:
                cancel_order_status = self.cancel_order(contract, open_order.order_id)
                if cancel_order_status is not None and cancel_order_status:
                    canceled_open_orders.append(cancel_order_status)
        return canceled_open_orders

    # Close position for a contract
    def close_position(self, contract: Contract):
        positions = self.get_positions()
        amount = positions[contract.symbol].amount
        result = None
        if amount > 0:
            result = self.place_order(contract, "SELL", abs(amount), "MARKET")
        elif amount < 0:
            result = self.place_order(contract, "BUY", abs(amount), "MARKET")
        return result

    ##############  UTILITY  ########################
    # Generate the signature to access signed requests
    def _generate_signature(self, data: typing.Dict) -> str:
        return hmac.new(SECRET_KEY.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    # Make requests to the API
    def _make_request(self, method: str, endpoint: str, data: typing.Dict):
        if method == "GET":
            try:
                response = requests.get(BASE_URL + endpoint, params=data, headers=self._HEADERS)
            except Exception as e:
                logger.error("Connection error while making % request to %s: %s", method, endpoint, e)
                return None
        elif method == "POST":
            try:
                response = requests.post(BASE_URL + endpoint, params=data, headers=self._HEADERS)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        elif method == "DELETE":
            try:
                response = requests.delete(BASE_URL + endpoint, params=data, headers=self._HEADERS)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        else:
            raise ValueError()
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making %s request to %s (error code %s)", method, endpoint, response.json(),
                         response.status_code)

    # Check price in filters
    def check_price(self, contract: Contract, price: float) -> bool:
        min_price = contract.min_price
        max_price = contract.max_price
        result = True
        if price is None or price > max_price or price < min_price:
            result = False
        return result

    # Check quantity in filters
    def check_quantity(self, contract: Contract, quantity: float) -> bool:
        min_quantity = contract.min_quantity
        max_quantity = contract.max_quantity
        result = True
        if quantity is None or quantity > max_quantity or quantity < min_quantity:
            result = False
        return result

    # Round price to price precision
    def round_price(self, contract: Contract, price: float) -> float:
        tick_size = (contract.tick_size)
        price_precision = (contract.price_precision)
        return round(round(price / tick_size) * tick_size, price_precision)

    # Round quantity to quantity precision
    def round_quantity(self, contract: Contract, price: float) -> float:
        step_size = (contract.step_size)
        quantity_precision = (contract.quantity_precision)
        return round(round(price / step_size) * step_size, quantity_precision)

    # Check if two prices are equals taking into account price precision
    def are_prices_equal(self, contract: Contract, price1: float, price2: float) -> bool:
        result = False
        if abs(price1 - price2) <= 1 / pow(10, -contract.price_precision):
            result = True
        return result


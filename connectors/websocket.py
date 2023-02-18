# Websocket
# Open the websocket and apply strategy
import requests
import time
import typing
import websocket
import threading
import json
from constants import *
from models import *
from strategy import GridTrading
import logging

logger = logging.getLogger()

class BinanceTestnetWebsocket:
    def __init__(self, strategy: GridTrading):
        self._strategy = strategy
        self._HEADERS = {'X-MBX-APIKEY': PUBLIC_KEY}
        # User Websockets
        self._user_ws = None
        t_user = threading.Thread(target=self._start_user_ws)
        t_user.start()

    ##################  USER WEBSOCKET  #########################
    # Open user websocket streams
    def _start_user_ws(self):
        self._listen_key = self._get_listen_key()['listenKey']
        self._user_ws = websocket.WebSocketApp(WSS_URL + "/" + self._listen_key, on_open=self._on_open,
                                               on_close=self._on_close, on_error=self._on_error,
                                               on_message=self._on_message)
        while True:
            try:
                # If still an error of connection
                # self._user_ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
                self._user_ws.run_forever()
            except Exception as e:
                logger.error("Binance User Websocket error in run_forever() method: %s", e)
            time.sleep(2)
    # Call back functions
    def _on_open(self, ws):
        logger.info("Binance User Websocket connection opened")
    def _on_close(self, ws):
        logger.warning("Binance User Websocket connection closed")
    def _on_error(self, ws, msg: str):
        logger.error("Binance User Websocket connection error: %s", msg)
    def _on_message(self, ws, msg: str):
        data = json.loads(msg)
        if "e" in data:
            # Get order updates
            if data['e'] == "ORDER_TRADE_UPDATE":
                data['o']['category'] = 'update'
                order = Order(data['o'])
                order.update_time = (time.time() * 1000)
                self._strategy.process_order(order)
            # Get account updates
            if data['e'] == "ACCOUNT_UPDATE":
                account_update = data['a']
                # Balances
                balance_updates = account_update['B']
                for balance_update in balance_updates:
                    balance_update = BalanceUpdate(balance_update)
                    balance_update.update_time = (time.time() * 1000)
                    #self._strategy.process_balance_update(balance_update)
                positions = account_update['P']
                # Positions
                for position in positions:
                    position['category'] = 'update'
                    position = Position(position)
                    position.update_time = (time.time() * 1000)
                    #self._strategy.process_position(position)

    ##############  UTILITY  ########################
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
    # Get listen key for user websocket
    def _get_listen_key(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        return self._make_request("POST", "/fapi/v1/listenKey", data)

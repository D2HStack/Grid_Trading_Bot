# Display orders ranked by price with mrk price and color depending on side
import tkinter as tk
import typing
from datetime import datetime
from interface.styling import *
from connectors.api import BinanceTestnetApi
from models import *
import logging

logger = logging.getLogger()

class Messages(tk.Frame):
    def __init__(self, api:BinanceTestnetApi, contract: Contract, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api
        self._headers = [{'label': 'Side', 'name': 'side'}, {'label': 'Price', 'name': 'price'}, {'label': 'Quantity', 'name': 'quantity'}]
        # Initial state of open orders
        self._open_orders = self._api.get_open_orders(contract)
        self._mark_price = self._api.get_mark_price(contract)
        self._build(self._open_orders, self._mark_price)
        for order in self._open_orders:
            print(str(order.order_id) + " " + str(order.symbol) + " " + str(order.side) + " " + str(order.price) + " " +str(order.quantity))

    # Build a table of orders
    def _build(self, orders: typing.List[OrderStatus], mark_price: MarkPrice):
        orders.append(OrderStatus({'i': 'mark_price', 's': mark_price.symbol, 'p': mark_price.mark_price, 'S': 'mark_price'}))
        orders = orders.sort('price')

        ''' 
        self._open_orders = self._api.get_open_orders(contract)
        self._open_orders_var = []
        self._open_orders_label = []
        mark_price = self._api.get_mark_price(contract)
        self._open_orders = self._open_orders.sort('price')
        for open_order in self._open_orders:
            row = self._open_orders.index(open_order)
            if open_order.side == "SELL":
                font = FG_COLOR_SELL
            elif open_order.side == "BUY":
                font = FG_COLOR_BUY
            open_order_var_temp = dict()
            open_order_var_temp['order_id'] = 
            
            for header
            self._open_orders_var.apppend(tk.StringVar())

            self._open_orders_label[index] = tk.Label(self, textvariable=self._open_orders_var[index], justify=tk.LEFT, bg=BG_COLOR,fg=font,font=BOLD_FONT)
            '''






            # Display
        self._
        self._messages_text = tk.Text(self, height=10, width=60, state=tk.DISABLED, bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self._messages_text.pack(side=tk.TOP)





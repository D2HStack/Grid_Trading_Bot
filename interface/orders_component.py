# Display orders ranked by price with mrk price and color depending on side
import tkinter as tk
import typing
from datetime import datetime
from interface.styling import *
from connectors.api import BinanceTestnetApi
from strategy import GridTrading
from models import *
import logging

logger = logging.getLogger()

class OrdersFrame(tk.Frame):
    def __init__(self, api: BinanceTestnetApi, strategy: GridTrading, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api
        self._strategy = strategy
        self._headers = [{'label': 'Side', 'name': 'side'}, {'label': 'Price', 'name': 'price'}, {'label': 'Quantity', 'name': 'quantity'}]
        self._initial = True
        self._grids = None
        self._orders = dict()
        self._order_var = dict()
        self._order_label = dict()
        # Position headers
        self._headers_label = dict()
        col = 0
        for header in self._headers:
            self._headers_label[header['name']] = tk.Label(self, text=header['label'],  justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            self._headers_label[header['name']].grid(row=0, column=col)
            col += 1

    # Build a table of orders
    def update(self):
        if self._strategy.get_active():
            orders = self._strategy.get_open_orders()
            orders.sort(key=lambda o: o.price, reverse=True)
            self._grids = self._strategy.get_grids()
            if self._initial:
                row = 1
                for order in orders:
                    if order is not None and order:
                        price_str = str(round(order.price, 8))
                        print(str(order.symbol) + " " + str(order.side) + " " + str(order.price))
                        self._orders[price_str] = order
                        self._order_var[price_str] = dict()
                        self._order_label[price_str] = dict()
                        col = 0
                        for header in self._headers:
                            name = header['name']
                            self._order_var[price_str][name] = tk.StringVar()
                            self._order_var[price_str][name].set(str(getattr(order, name)))
                            self._order_label[price_str][name] = tk.Label(self, textvariable=self._order_var[price_str][name], justify=tk.LEFT, bg=BG_COLOR, fg=self._font(order), font=BOLD_FONT)
                            self._order_label[price_str][name].grid(row=row, column=col)
                            col += 1
                        row += 1
                self._initial = False
            else:
                row = 1
                for price_str in self._orders:
                    index = orders.index(self._orders[price_str])



    # Change font color depending on side
    def _font(self, order: OrderStatus) -> str:
        if order.side == "BUY":
            return FG_COLOR_BUY
        elif order.side == "SELL":
            return FG_COLOR_SELL


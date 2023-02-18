# Display orders ranked by price with mrk price and color depending on side
from tkinter import *
import typing
import datetime
from interface.styling import *
from connectors.api import BinanceTestnetApi
from strategy import GridTrading
from models import *
import logging

logger = logging.getLogger()

class OrdersFrame(Frame):
    def __init__(self, headers: typing.List[dict], title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._headers = headers
        self._length = 0
        self._order_vars = []
        self._order_labels = []
        # Build headers
        self._headers_label = []
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self._title = Label(self, text=title, font=TITLE_FONT)
        self._title.grid(row=0, column=0, columnspan=4, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=W+E)
        for col, header in enumerate(self._headers):
            self._headers_label.append(Label(self, text=header['label'], font=LABEL_FONT))
            self._headers_label[col].grid(row=1, column=col,  ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=W+E)

    # Update a table of orders
    def update(self, orders: typing.List[Order]) -> dict:
        sort_result = self._sort_orders(orders)
        if sort_result['sorted']:
            orders_length = len(orders)
            current_length = len(self._order_vars)
            if orders_length >= current_length:
                for row,order in enumerate(orders):
                    if row < current_length:
                        self._refresh_order_display(order, row)
                    else:
                        self._build_order_display(order, row)
            else:
                for row, order in enumerate(orders):
                        self._refresh_order_display(order, row)
                for row in range(orders_length, current_length):
                    self._remove_order_display(row)
            return {'msg': 'List of orders is displayed', 'displayed': True, 'data': orders}
        else:
            return {'msg': 'List of orders is empty', 'displayed': False, 'data': orders}

    # Change font color depending on side
    def _font(self, order: Order) -> str:
        if order is not None and order:
            if order.side == "BUY":
                return FG_COLOR_BUY
            elif order.side == "SELL":
                return FG_COLOR_SELL
        else:
            return FG_COLOR

    def _sort_orders(self, orders: typing.List[Order]):
        if orders is not None:
            orders.sort(key=lambda o: o.price, reverse=True)
            return {'msg': 'List of orders has been sorted', 'sorted': True, 'data': orders}
        else:
            return {'msg': 'List of orders is empty', 'sorted': False, 'data': orders}

    def _build_order_display(self, order:Order, row: int):
        self._order_vars.append([])
        self._order_labels.append([])
        for col, header in enumerate(self._headers):
            name = header['name']
            self._order_vars[row].append(StringVar())
            self._order_labels[row].append(
                Label(self, textvariable=self._order_vars[row][col], fg=self._font(order), font=BOLD_FONT))
            self._order_vars[row][col].set(header['func'](getattr(order, name)))
            self._order_labels[row][col].grid(row=row + 2, column=col)

    def _remove_order_display(self, row: int):
        for col, header in enumerate(self._headers):
            self._order_vars[row][col].set("")

    def _refresh_order_display(self, order:Order, row: int):
        for col, header in enumerate(self._headers):
            name = header['name']
            self._order_labels[row][col].config(fg=self._font(order))
            self._order_vars[row][col].set(header['func'](getattr(order, name)))

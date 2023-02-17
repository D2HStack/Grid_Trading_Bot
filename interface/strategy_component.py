# Strategy frame
import tkinter as tk
from interface.styling import *
from strategy import GridTrading
from interface.messages_component import Messages
from models import *
import logging

logger = logging.getLogger()

class StrategyFrame(tk.Frame):
    def __init__(self, strategy: GridTrading, messages: Messages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._strategy = strategy
        self._messages = messages
        self._param_title = "Parameters"
        self._param_headers = [{'name': 'symbol', 'label': 'Contract', 'value': None}, {'name': 'lower_price', 'label': 'Lower Price', 'value': None}, {'name': 'upper_price', 'label': 'Upper Price', 'value': None}, {'name': 'grids', 'label': 'Grids', 'value': None}, {'name': 'initial_margin', 'label': 'Initial Margin', 'value': None}, ]
        self._param_labels = dict()
        self._param_entries = dict()
        self._order_title = "Order Monitoring"
        self._order_headers = [{'name': 'open_orders', 'label': 'Open Orders'}, {'name': 'filled_orders', 'label': 'Filled Orders'}, {'name': 'unmatched_orders', 'label': 'Unmatched Orders'}, {'name': 'matched_orders', 'label': 'Matched Orders'},]
        self._order_labels = dict()
        self._order_vars = dict()
        self._pnl_title = "P&L Monitoring"
        self._pnl_headers = [{'name': 'entry_price', 'label': 'Entry Price'}, {'name': 'mark_price', 'label': 'Mark Price'}, {'name': 'current_margin', 'label': 'Current Margin'}, {'name': 'unrealized_profit', 'label': 'Unrealized Profit'}, {'name': 'realized_profit', 'label': 'Realized Profit'}, {'name': 'total_profit', 'label': 'Total Profit'}]
        self._pnl_labels = dict()
        self._pnl_vars = dict()

        ################################  FRAMES AND WIDGETS  ###########################################################
        # Strategy parameters
        self._param_title_label = tk.Label(self, text=self._param_title, justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT)
        self._param_title_label.pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        for index,param in enumerate(self._param_headers):
            name = param['name']
            self._param_labels[name] = tk.Label(self, text=self._param_headers[index]['label'],  justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            self._param_labels[name].pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
            self._param_entries[name] = tk.Entry(self, fg=FG_COLOR, justify=tk.LEFT, insertbackground=FG_COLOR, bg=BG_COLOR_2)
            self._param_entries[name].bind("<Return>", self._on_return(param))
            self._param_entries[name].pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        self._create_button = tk.Button(self, text="CREATE", font=BUTTON_FONT,
                                                 command=self._on_submit_create, bg=BG_COLOR_2,
                                                 fg=FG_COLOR_BUTTON)
        self._create_button.pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        # Order monitoring
        self._order_title_label = tk.Label(self, text=self._order_title, justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR,
                                            font=TITLE_FONT)
        self._order_title_label.pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        for index, indicator in enumerate(self._order_headers):
            name = indicator['name']
            self._order_vars[name] = tk.StringVar()
            self._order_labels[name] = tk.Label(self, textvariable=self._order_vars[name], justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            self._order_labels[name].pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        # P&L
        self._pnl_title_label = tk.Label(self, text=self._pnl_title, justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR,
                                           font=TITLE_FONT)
        self._pnl_title_label.pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        for index, indicator in enumerate(self._pnl_headers):
            name = indicator['name']
            self._pnl_vars[name] = tk.StringVar()
            self._pnl_labels[name] = tk.Label(self, textvariable=self._pnl_vars[name], justify=tk.LEFT, bg=BG_COLOR,
                                                fg=FG_COLOR, font=BOLD_FONT)
            self._pnl_labels[name].pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)
        self._close_button = tk.Button(self, text="CLOSE", font=BUTTON_FONT,
                                        command=self._on_submit_close, bg=BG_COLOR_2,
                                        fg=FG_COLOR_BUTTON, state='disabled')
        self._close_button.pack(side=tk.TOP, padx=GLOBAL_PAD, pady=GLOBAL_PAD)

    # Call back function on <Return>
    def _on_return(self, param: str):
        def _get_value(event):
            entered_value = event.widget.get()
            index = self._param_headers.index(param)
            if entered_value is not None and entered_value:
                self._param_headers[index]['value'] = entered_value
                self._messages.add_msg(
                    str(self._param_headers[index]['label']) + " updated to:" + str(self._param_headers[index]['value']))
                if index < len(self._param_headers) - 1:
                    next_param = self._param_headers[index+1]
                    self._param_entries[next_param['name']].focus_set()
            else:
                self._messages.add_msg("Nothing entered")
        return _get_value

    ################################  ONSUBMIT BUTTON  ###########################################################
    # Create button
    def _on_submit_create(self):
        # Disable button and entries and build the params for create strategy method
        self._create_button.config(state="disabled")
        self._close_button.config(state="normal")
        params = dict()
        for index,param in enumerate(self._param_headers):
            name = param['name']
            params[name] = self._param_headers[index]['value']
            self._param_entries[name].config(state="disabled")
        params = ({'symbol': 'ETHUSDT', 'lower_price': 1680, 'upper_price': 1710, 'grids': 30, 'initial_margin': 1000})
        msg = self._strategy.create(GridParam(params))['msg']
        self._messages.add_msg(msg)

    # Close button
    def _on_submit_close(self):
        # Enable button and entries and build the params for create strategy method
        # Disable button and entries and build the params for create strategy method
        self._create_button.config(state="normal")
        self._close_button.config(state="disabled")
        params = dict()
        for param in self._param_headers:
            index = self._param_headers.index(param)
            name = param['name']
            self._param_entries[name].config(state="normal")
        msg = self._strategy.close()
        self._messages.add_msg(msg)

    # Update the orders monitoring
    def update_orders(self):
        for index,indicator in enumerate(self._order_headers):
            name = indicator['name']
            self._order_vars[name].set(str(self._order_headers[index]['label']) + ": " + str(len(self._strategy.get_value(name))))

    # Update the pnl monitoring
    def update_pnl(self):
        for index, indicator in enumerate(self._pnl_headers):
            name = indicator['name']
            self._pnl_vars[name].set(str(self._pnl_headers[index]['label']) + ": " + str(round(self._strategy.get_value(name), 3)))
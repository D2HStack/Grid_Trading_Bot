# Strategy frame
from tkinter import *
from interface.styling import *
from strategy import GridTrading
from interface.messages_component import Messages
from models import *
import logging

logger = logging.getLogger()

class StrategyFrame(Frame):
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
        self._order_titles = dict()
        self._order_labels = dict()
        self._order_vars = dict()
        self._pnl_title = "P&L Monitoring"
        self._pnl_headers = [{'name': 'entry_price', 'label': 'Entry Price'}, {'name': 'mark_price', 'label': 'Mark Price'}, {'name': 'current_margin', 'label': 'Current Margin'}, {'name': 'unrealized_profit', 'label': 'Unrealized Profit'}, {'name': 'realized_profit', 'label': 'Realized Profit'}, {'name': 'total_profit', 'label': 'Total Profit'}]
        self._pnl_titles = dict()
        self._pnl_labels = dict()
        self._pnl_vars = dict()

        ################################  FRAMES AND WIDGETS  ###########################################################
        # Strategy parameters
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self._param_title_label = Label(self, text=self._param_title, font=TITLE_FONT)
        self._param_title_label.grid(column=0, row=0, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        for row,param in enumerate(self._param_headers):
            name = param['name']
            self._param_labels[name] = Label(self, text=self._param_headers[row]['label'], font=LABEL_FONT)
            self._param_labels[name].grid(column=0, row=row+1, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
            self._param_entries[name] = Entry(self, font=FONT)
            self._param_entries[name].bind("<Return>", self._on_return(param))
            self._param_entries[name].grid(column=1, row=row+1, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        self._create_button = Button(self, text="CREATE", command=self._on_submit_create, font=BUTTON_FONT, height=BUTTON_HEIGHT)
        self._create_button.grid(column=0, row=len(self._param_headers)+1, columnspan=2, ipadx=IPADX, ipady=IPADY, padx=BUTTON_PADX, pady=PADY, sticky=BUTTON_STICKY)
        # Order monitoring
        self._order_title_label = Label(self, text=self._order_title, font=TITLE_FONT)
        self._order_title_label.grid(column=0, row=len(self._param_headers)+2, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        for row,indicator in enumerate(self._order_headers):
            name = indicator['name']
            self._order_titles[name] = Label(self, text=indicator['label'], font=LABEL_FONT, )
            self._order_titles[name].grid(column=0, row=len(self._param_headers) + 3 + row, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
            self._order_vars[name] = StringVar()
            self._order_labels[name] = Label(self, textvariable=self._order_vars[name], font=LABEL_FONT)
            self._order_labels[name].grid(column=1, row=len(self._param_headers)+3+row,ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        # P&L
        self._pnl_title_label = Label(self, text=self._pnl_title,font=TITLE_FONT)
        self._pnl_title_label.grid(column=0, row=len(self._param_headers) + 3 + len(self._order_headers), columnspan=2, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        for row, indicator in enumerate(self._pnl_headers):
            name = indicator['name']
            self._pnl_titles[name] = Label(self, text=indicator['label'], font=LABEL_FONT)
            self._pnl_titles[name].grid(column=0, row=len(self._param_headers) + 4 + len(self._order_headers) + row, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
            self._pnl_vars[name] = StringVar()
            self._pnl_labels[name] = Label(self, textvariable=self._pnl_vars[name], font=LABEL_FONT)
            self._pnl_labels[name].grid(column=1, row=len(self._param_headers) + 4 + len(self._order_headers) + row, ipadx=IPADX, ipady=IPADY, padx=PADX, pady=PADY, sticky=STICKY)
        self._close_button = Button(self, text="CLOSE",command=self._on_submit_close, state='disabled', font=BUTTON_FONT, height=BUTTON_HEIGHT)
        self._close_button.grid(column=0, row=len(self._param_headers) + 4 + len(self._order_headers) + len(self._pnl_headers) + 1, columnspan=2, ipadx=IPADX, ipady=IPADY, padx=BUTTON_PADX, pady=PADY, sticky=BUTTON_STICKY)

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
            self._order_vars[name].set(str(len(self._strategy.get_value(name))))

    # Update the pnl monitoring
    def update_pnl(self):
        for index, indicator in enumerate(self._pnl_headers):
            name = indicator['name']
            self._pnl_vars[name].set(str(round(self._strategy.get_value(name), 3)))
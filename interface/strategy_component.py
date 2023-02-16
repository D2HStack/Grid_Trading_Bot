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
        self._params = [{'name': 'contract', 'label': 'Contract', 'value': None}, {'name':'lower_price', 'label': 'Lower Price', 'value': None}, {'name': 'upper_price', 'label': 'Upper Price', 'value': None}, {'name': 'grids', 'label': 'Grids', 'value': None}, {'name': 'initial_margin', 'label': 'Initial Margin', 'value': None}, ]
        self._strategy = strategy
        self._messages = messages
        self._labels = dict()
        self._entries = dict()
        self._on_returns = dict()

        ################################  FRAMES AND WIDGETS  ###########################################################
        for param in self._params:
            index = self._params.index(param)
            name = param['name']
            self._labels[name] = tk.Label(self, text=self._params[index]['label'],  justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            self._labels[name].pack(side=tk.TOP)
            self._entries[name] = tk.Entry(self, fg=FG_COLOR, justify=tk.LEFT, insertbackground=FG_COLOR, bg=BG_COLOR_2)
            self._entries[name].bind("<Return>", self._on_return(param))
            self._entries[name].pack(side=tk.TOP)
        self._create_button = tk.Button(self, text="CREATE", font=BUTTON_FONT,
                                                 command=self._on_submit_create, bg=BG_COLOR_2,
                                                 fg=FG_COLOR_BUTTON)
        self._create_button.pack(side=tk.TOP)
        self._close_button = tk.Button(self, text="CLOSE", font=BUTTON_FONT,
                                        command=self._on_submit_close, bg=BG_COLOR_2,
                                        fg=FG_COLOR_BUTTON, state='disabled')
        self._close_button.pack(side=tk.TOP)

    # Call back function on <Return>
    def _on_return(self, param: str):
        def _get_value(event):
            entered_value = event.widget.get()
            index = self._params.index(param)
            if entered_value is not None and entered_value:
                self._params[index]['value'] = entered_value
                self._messages.add_msg(
                    str(self._params[index]['label']) + " updated to:" + str(self._params[index]['value']))
                if index < len(self._params) - 1:
                    next_param = self._params[index+1]
                    self._entries[next_param['name']].focus_set()
            else:
                logger.warning("Nothing entered")
        return _get_value

    ################################  ONSUBMIT BUTTON  ###########################################################
    # Create button
    def _on_submit_create(self):
        # Disable button and entries and build the params for create strategy method
        self._create_button.config(state="disabled")
        self._close_button.config(state="normal")
        params = dict()
        for param in self._params:
            index = self._params.index(param)
            name = param['name']
            params[name] = self._params[index]['value']
            self._entries[name].config(state="disabled")
        # For testing
        params = GridParam({'symbol': 'ETHUSDT', 'lower_price': 1000, 'upper_price': 2000, 'grids': 5, 'initial_margin': 1000})
        msg = self._strategy.create(params)['msg']
        self._messages.add_msg(msg)

    # Close button
    def _on_submit_close(self):
        # Enable button and entries and build the params for create strategy method
        # Disable button and entries and build the params for create strategy method
        self._create_button.config(state="normal")
        self._close_button.config(state="disabled")
        params = dict()
        for param in self._params:
            index = self._params.index(param)
            name = param['name']
            #params[name] = self._params[index]['value']
            self._entries[name].config(state="normal")
        msg = self._strategy.close()
        self._messages.add_msg(msg)

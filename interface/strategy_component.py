# Strategy frame
import tkinter as tk
from interface.styling import *
from strategy import GridTrading
from interface.messages_component import Messages
import logging

logger = logging.getLogger()

class StrategyFrame(tk.Frame):
    def __init__(self, strategy: GridTrading, messages: Messages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params = {'contract': {'label': 'Contract', 'value': None}, 'lower_price': {'label': 'Lower Price', 'value': None}, 'upper_price': {'label': 'Upper Price', 'value': None}, 'grids': {'label': 'Grids', 'value': None}, 'initial_margin': {'label': 'Initial Margin', 'value': None}, }
        self._strategy = strategy
        self._messages = messages
        self._labels = dict()
        self._entries = dict()
        self._on_returns = dict()

        ################################  FRAMES AND WIDGETS  ###########################################################
        for param in self._params:
            self._labels[param] = tk.Label(self, text=self._params[param]['label'],  justify=tk.LEFT, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            self._labels[param].pack(side=tk.TOP)
            self._entries[param] = tk.Entry(self, fg=FG_COLOR, justify=tk.LEFT, insertbackground=FG_COLOR, bg=BG_COLOR_2)
            self._entries[param].bind("<Return>", self._on_return(param))
            self._entries[param].pack(side=tk.TOP)
        self._create_button = tk.Button(self, text="CREATE", font=BUTTON_FONT,
                                                 command=self._on_submit_create, bg=BG_COLOR_2,
                                                 fg=FG_COLOR_BUTTON)
        self._create_button.pack(side=tk.TOP)

    # Call back function on <Return>
    def _on_return(self, param: str):
        def _get_value(event):
            entered_value = event.widget.get()
            if entered_value is not None and entered_value:
                self._params[param]['value'] = entered_value
                self._messages.add_msg(
                    str(self._params[param]['label']) + " updated to:" + str(self._params[param]['value']))
            else:
                logger.warning("Nothing entered")
        return _get_value

    ################################  ONSUBMIT BUTTON  ###########################################################
    # Create button
    def _on_submit_create(self):
        # Disable button and entries and build the params for create strategy method
        self._create_button.config(state="disabled")
        params = dict()
        for param in self._params:
            params[param] = self._params[param]['value']
            self._entries[param].config(state="disabled")
        self._strategy.create(params)
        self._messages.add_msg("Grid is lanuched !")

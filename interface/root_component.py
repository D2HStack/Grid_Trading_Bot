# Root
# Display the interface

import tkinter as tk
from interface.styling import *
from strategy import GridTrading
from connectors.api import BinanceTestnetApi
from connectors.websocket import BinanceTestnetWebsocket
from interface.messages_component import Messages
from interface.strategy_component import StrategyFrame
import logging

logger = logging.getLogger()

class Root(tk.Tk):
    def __init__(self, strategy: GridTrading, api: BinanceTestnetApi, websocket: BinanceTestnetWebsocket):
        super().__init__()
        self._strategy = strategy
        self._api = api
        self._websocket = websocket
        self._messages_frame = Messages()
        # Window
        self.title("Grid Trading")
        # Divide the window in 2 frames
        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT)
        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side=tk.RIGHT)
        # Frames
        self._messages_frame = Messages(self._right_frame, bg=BG_COLOR)
        self._messages_frame.pack(side=tk.TOP)
        self._strategy_frame = StrategyFrame(self._strategy, self._messages_frame, self._left_frame, bg=BG_COLOR)
        self._strategy_frame.pack(side=tk.TOP)
        # Initialising update
        self._update_ui()

    # Udpate the UI
    def _update_ui(self):
        try:
            # Update frames
            self._messages_frame.update_msg()
            logger.info("Messages updated")

        except RuntimeError as e:
            print("Error while updating interface: %s", e)
            # Loop on itself after x milliseconds
        self.after(1500, self._update_ui)
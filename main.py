# Main
# Launch the root component, the interface in tkinter with a strategy and connectors websocket and api

from interface.root_component import Root
from strategy import GridTrading
from connectors.api import BinanceTestnetApi
from connectors.websocket import BinanceTestnetWebsocket
if __name__ == '__main__':
    api = BinanceTestnetApi()
    strategy = GridTrading(api)
    websocket = BinanceTestnetWebsocket(strategy)
    # Create an instance of root component
    root = Root(strategy, api, websocket)
    # Create a loop to keep the window open
    root.mainloop()
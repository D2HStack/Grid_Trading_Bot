# Main
# Launch the root component, the interface in tkinter with a strategy and connectors websocket and api

from interface.root_component import Root
from strategy import GridTrading
from connectors.api import BinanceTestnetApi
from connectors.websocket import BinanceTestnetWebsocket

##############################  Configure logging  ############################################
import logging
# Create debug, info, warning, error messages
logger = logging.getLogger() # create an instance of logging object
logger.setLevel(logging.DEBUG)
# Create and format the streamhandler
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
# Write messages in info.log
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':
    api = BinanceTestnetApi()
    strategy = GridTrading(api)
    websocket = BinanceTestnetWebsocket(strategy)
    # Create an instance of root component
    root = Root(strategy, api, websocket)
    # Create a loop to keep the window open
    root.mainloop()
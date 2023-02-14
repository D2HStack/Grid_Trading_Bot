# Strategy
# Define the strategy

from connectors.api import BinanceTestnetApi
import logging

logger = logging.getLogger()

class GridTrading:
    def __init__(self, api: BinanceTestnetApi):
        print("Hello from GridTrading")

    def create(self, params: dict):
        logger.info("Grid created")
<h1><a href="https://github.com/ez-crypto/grid_trading_bot">EZ-Crypto - Grid Trading Bot</a></h1>


Open source grid trading bot in python using   [Binance Futures Testnet](https://testnet.binancefuture.com/en/futures/BTCUSDT) API and websocket.

- 👉 Live demo on <a href="https://www.ez-crypto.fr/"><img src="https://res.cloudinary.com/hoang23/image/upload/v1676736667/logo-ez-crypto-text-purple_tbgtwi.svg" height="15"></a> 
- 👉 Get your API keys on [Binance Futures Testnet](https://testnet.binancefuture.com/en/futures/BTCUSDT)
- 👉 API documentation on [Binance Futures Testnet API](https://binance-docs.github.io/apidocs/#change-log)

## Features
- ✅ Coded in Python without many dependencies.
- ✅ Simple form to launch the grid.
- ✅ Dashboard to monitor orders, trades, unrealized and realized profits.

<img src="https://res.cloudinary.com/hoang23/image/upload/v1676736318/grid-trading-python-screenshot_iwccdb.png"/>

## Build using PyCharm

👉 **Step 1** - Download the code from the GH repository (using `GIT`)
```bash
git clone https://github.com/ez-crypto/grid_trading_bot
cd grid_trading_bot
```

👉 **Step 2** - Install modules
```bash
 pip install -r requirements.txt
```

👉 **Step 3** - Set up environment variables in 
- Create a `.env` file in project directory
- Write your public and secret keys as PUBLIC_KEY and SECRET_KEY

## Codebase structure

The project is coded using a simple and intuitive structure.

```bash
< PROJECT ROOT >
   |
   |-- connectors/                            
   |-- api.py                         # Exchange API
   |-- websocket.py                   # Exchange Websocket
   |
   |-- interfaces/                            
   |    |-- messages_component.py     # Messages to User
   |    |-- orders_component.py       # Orders displayed by price and side
   |    |-- root_component.py         # Root
   |    |-- strategy_component.py     # Set and monitoring of the strategy
   |    |-- styling.py                # Styles of Tkinter window
   |     
   |-- .env                           # Env variables
   |-- constants.py                   # Global constants
   |-- main.py                        # Start
   |-- models.py                      # Data structure models
   |-- requirements.txt               # Project Dependencies
   |-- strategy.py                    # Manage the strategy
   |
   |-- ************************************************************************
```
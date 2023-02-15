# Balances data from Account/Trades Endpoints /  Account Information V2 (USER_DATA)
class Balance:
    def __init__(self, info):
        self.asset = info['asset']
        self.initial_margin = float(info['initialMargin'])
        self.maintenance_margin = float(info['maintMargin'])
        self.margin_balance = float(info['marginBalance'])
        self.wallet_balance = float(info['walletBalance'])
        self.unrealized_profit = float(info['unrealizedProfit'])
        self.max_withdraw_amount = float(info['maxWithdrawAmount'])

# Contracts data from Market Data Endpoints /  Exchange Information in key "symbol" and list
class Contract:
    def __init__(self, info):
        self.symbol = info['symbol']
        self.base_asset = info['baseAsset']
        self.quote_asset = info['quoteAsset']
        self.maint_margin_percent = float(info['maintMarginPercent']) # originally a string
        self.price_precision = (info['pricePrecision'])
        self.quantity_precision = ((info['quantityPrecision']))
        self.required_margin_percent = float(info['requiredMarginPercent']) # originally a string
        self.max_price = float(info['filters'][0]['maxPrice'])
        self.min_price = float(info['filters'][0]['minPrice'])
        self.tick_size = float(info['filters'][0]['tickSize'])
        self.max_quantity = float(info['filters'][1]['maxQty'])
        self.min_quantity = float(info['filters'][1]['minQty'])
        self.step_size = float(info['filters'][1]['stepSize'])
        self.max_num_orders = float(info['filters'][3]['limit'])

# Status of orders from Account/Trades Endpoints/Query Order (USER_DATA)
class OrderStatus:
    def __init__(self, info):
        self.symbol = (info['symbol'])
        self.order_id = (info['orderId'])
        self.price = float(info['price'])
        self.quantity = float(info['origQty'])
        self.filled_quantity = float(info['executedQty'])
        self.status = (info['status'])
        self.type = (info['type'])
        self.side = (info['side'])
        self.order_time = 0
# Order Update from user stream "ORDER_TRADE_UPDATE"
class OrderUpdate:
    def __init__(self, info):
        self.symbol = (info['s'])
        self.order_id = (info['i'])
        self.price = float(info['p'])
        self.quantity = float(info['q'])
        self.filled_quantity = float(info['z'])
        self.status = (info['X'])
        self.type = (info['o'])
        self.side = (info['S'])
        self.order_time = (info['T'])
        self.update_time = 0
        self.avg_price = float(info['ap'])
# positions from Account/Trades Endpoints/Position Information (USER_DATA)
class PositionStatus:
    def __init__(self, info):
        self.symbol = (info['symbol'])
        self.amount = float(info['positionAmt'])
        self.liquidation_price = float(info['liquidationPrice'])
        self.mark_price = float(info['markPrice'])
        self.unrealized_profit = float(info['unRealizedProfit'])
# Positions from user websocket Event: Balance and Position Update
class PositionUpdate:
    def __init__(self, info):
        self.symbol = (info['s'])
        self.amount = float(info['pa'])
        self.entry_price = float(info['ep'])
        self.accumulated_realized = float(info['cr'])
        self.update_time = 0
# Balances from user websocket Event: Balance and Position Update
class BalanceUpdate:
    def __init__(self, info):
        self.asset = (info['a'])
        self.wallet_balance = float(info['wb'])
        self.update_time = 0
# Market price
class MarkPrice:
    def __init__(self, info):
        self.symbol = (info['symbol'])
        self.mark_price = float(info['markPrice'])
        self.time = 0


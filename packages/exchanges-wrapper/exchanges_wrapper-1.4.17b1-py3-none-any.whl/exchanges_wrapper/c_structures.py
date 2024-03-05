from decimal import Decimal

REST_RATE_LIMIT_INTERVAL = {
    "bitfinex": {
        "default": 0.6667,  # 90 requests per minute
    },
}


class OrderTradesEvent:
    def __init__(self, event_data: {}):
        self.symbol = event_data["symbol"]
        self.client_order_id = event_data["clientOrderId"]
        self.side = "BUY" if event_data["isBuyer"] else "SELL"
        self.order_type = "LIMIT"
        self.time_in_force = "GTC"
        self.order_quantity = event_data["origQty"]
        self.order_price = event_data["orderPrice"]
        self.stop_price = "0"
        self.iceberg_quantity = "0"
        self.order_list_id = -1
        self.original_client_id = ""
        self.execution_type = "TRADE"
        self.order_reject_reason = "NONE"
        self.order_id = event_data["orderId"]
        self.last_executed_quantity = event_data["qty"]
        self.cumulative_filled_quantity = event_data["executedQty"]
        self.order_status = event_data["status"]
        self.last_executed_price = event_data["price"]
        self.commission_amount = event_data["commission"]
        self.commission_asset = event_data["commissionAsset"]
        self.transaction_time = event_data["time"]
        self.trade_id = event_data["id"]
        self.ignore_a = int()
        self.in_order_book = True
        self.is_maker_side = event_data["isMaker"]
        self.ignore_b = False
        self.order_creation_time = event_data["time"]
        self.quote_asset_transacted = event_data["cummulativeQuoteQty"]
        self.last_quote_asset_transacted = event_data["quoteQty"]
        self.quote_order_quantity = str(Decimal(self.order_quantity) * Decimal(self.order_price))


def order(res: {}, response_type=None) -> {}:
    if response_type:
        return {
            "symbol": res.get('symbol'),
            "origClientOrderId": res.get('origClientOrderId'),
            "orderId": res.get('orderId'),
            "orderListId": res.get('orderListId'),
            "clientOrderId": res.get('clientOrderId'),
            "transactTime": res.get('time'),
            "price": res.get('price'),
            "origQty": res.get('origQty'),
            "executedQty": res.get('executedQty'),
            "cummulativeQuoteQty": res.get('cummulativeQuoteQty'),
            "status": res.get('status'),
            "timeInForce": res.get('timeInForce'),
            "type": res.get('type'),
            "side": res.get('side'),
        }
    elif response_type is None:
        return {
            "symbol": res.get('symbol'),
            "orderId": res.get('orderId'),
            "orderListId": res.get('orderListId'),
            "clientOrderId": res.get('clientOrderId'),
            "price": res.get('price'),
            "origQty": res.get('origQty'),
            "executedQty": res.get('executedQty'),
            "cummulativeQuoteQty": res.get('cummulativeQuoteQty'),
            "status": res.get('status'),
            "timeInForce": res.get('timeInForce'),
            "type": res.get('type'),
            "side": res.get('side'),
            "stopPrice": res.get('stopPrice'),
            "icebergQty": res.get('icebergQty'),
            "time": res.get('time'),
            "updateTime": res.get('updateTime'),
            "isWorking": res.get('isWorking'),
            "origQuoteOrderQty": res.get('origQuoteOrderQty'),
        }
    else:
        return {
            "symbol": res.get('symbol'),
            "orderId": res.get('orderId'),
            "orderListId": res.get('orderListId'),
            "clientOrderId": res.get('clientOrderId'),
            "price": res.get('price'),
            "origQty": res.get('origQty'),
            "executedQty": res.get('executedQty'),
            "cummulativeQuoteQty": res.get('cummulativeQuoteQty'),
            "status": res.get('status'),
            "timeInForce": res.get('timeInForce'),
            "type": res.get('type'),
            "side": res.get('side'),
        }

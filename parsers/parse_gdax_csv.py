import csv
from utils.timestamps import timestamp_to_datetime, datetime_in_threshold

TIMESTAMP = 0
AMOUNT = 3
ASSET = 4
SPOT_VALUE_USD = 5
TOTAL_VALUE_USD = 6
TAX_TYPE = 7

def parse_gdax(gdax_file):
    gdax_csv = open(gdax_file, 'r')

    taxable_terms = ['sale', 'purchase', 'trade_fee']
    taxable_txs = []

    # STEP 1: Group Tx's into groups based on time
    time_threshold_sec = 5

    last_timestamp = None
    group = []
    for row in gdax_csv:
        row_cols = row.split(',')
        if row_cols[TIMESTAMP] == 'Date':
            continue
        if not last_timestamp:
            last_timestamp = timestamp_to_datetime(row_cols[TIMESTAMP])
        if row_cols[TAX_TYPE] not in taxable_terms:
            # if it isn't a buy, sell or fee we can ignore
            continue
        if row_cols[TAX_TYPE] != taxable_terms[2] and row_cols[ASSET] == 'USD':
            # we can infer USD "buys" and "sells"
            continue
        new_timestamp = timestamp_to_datetime(row_cols[TIMESTAMP])
        in_range = datetime_in_threshold(new_timestamp, last_timestamp, time_threshold_sec)

        tx_data = {
            "timestamp": new_timestamp,
            "asset": row_cols[ASSET],
            "amount": row_cols[AMOUNT],
            "type": row_cols[TAX_TYPE],
            "value_usd": row_cols[TOTAL_VALUE_USD],
        }

        if in_range:
            group.append(tx_data)
        else:
            taxable_txs.append(group)
            group = [tx_data]

        last_timestamp = new_timestamp

    # STEP 2 determine type of event BUY or SELL
    SELL = 0
    BUY = 1

    buys = []
    sells = []
    for event in taxable_txs:
        sell_asset = None
        buy_asset = None
        sell_value = 0
        buy_value = 0
        sell_amount = 0
        buy_amount = 0
        fees = 0

        for tx in event:
            # sell event
            if tx["type"] == taxable_terms[0] and tx["asset"] is not 'USD':
                sell_value += abs(float(tx["value_usd"]))
                if not sell_asset:
                    sell_asset = tx["asset"]
                # can't fix asset types within a category or we got problems
                assert(tx["asset"] == sell_asset)
                sell_amount += abs(float(tx["amount"]))
            elif tx["type"] == taxable_terms[1] and tx["asset"] is not 'USD':
                buy_value += abs(float(tx["value_usd"]))
                if not buy_asset:
                    buy_asset = tx["asset"]
                # can't fix asset types within a category or we got problems
                assert(tx["asset"] == buy_asset)
                buy_amount += abs(float(tx["amount"]))
            elif tx["type"] == taxable_terms[2]:
                fees += abs(float(tx["value_usd"]))

        if buy_asset:
            # if we didn't sell this trade add the fee here
            if not sell_asset:
                # if its a buy then the fee was an extra part of the cost
                buy_value += fees
            buys.append({
                "timestamp": event[-1]["timestamp"], # use the latest time as timestamp
                "asset": buy_asset,
                "amount": buy_amount,
                "value": buy_value,
                "price_per_unit": (buy_value / buy_amount),
                "exchange": "GDAX"
            })
        if sell_asset:
            # if it was a sell, the fee decreased our return value
            sell_value -= fees
            sells.append({
                "timestamp": event[-1]["timestamp"], # use the latest time as timestamp
                "asset": sell_asset,
                "amount": sell_amount,
                "value": sell_value,
                "price_per_unit": (sell_value / sell_amount),
                "exchange": "GDAX"
            })

    return buys, sells

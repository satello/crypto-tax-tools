import csv
from datetime import datetime
from utils.timestamps import timestamp_to_datetime

DATE = 0
TIME = 1
TYPE = 2
SYMBOL = 3
AMOUNT = 7
FEE = 8
BTC_AMT = 10
ETH_AMT = 13
# trade types
ETH = 'ETHUSD'
BTC = 'BTCUSD'

def parse_gemini(gemini_file):
    with open(gemini_file) as f:
        reader = csv.reader(f)
        taxable_terms = ['Buy', 'Sell']
        taxable_txs = []

        buys = []
        sells = []
        for row_cols in reader:
            if row_cols[0] == 'Date':
                continue
            # taxable events
            if row_cols[TYPE] in taxable_terms:
                year, month, day = row_cols[DATE].split('-')
                hour, minute, second = row_cols[TIME].split(':')
                timestamp = timestamp_to_datetime('%s-%s-%sT%s:%s:%sZ' % (year, month, day, hour, minute, second.split(".")[0]))
                value = gemini_amount_to_float(row_cols[AMOUNT]) + gemini_amount_to_float(row_cols[FEE])

                # ETH
                if row_cols[SYMBOL] == ETH:
                    amount = gemini_asset_to_float(row_cols[ETH_AMT])
                    # buy
                    if row_cols[TYPE] == taxable_terms[0]:
                        buys.append({
                            "timestamp": timestamp,
                            "asset": 'ETH',
                            "amount": amount,
                            "value": value,
                            "price_per_unit": (value / amount),
                            "exchange": "GEMINI"
                        })
                    elif row_cols[TYPE] == taxable_terms[1]:
                        sells.append({
                            "timestamp": timestamp,
                            "asset": 'ETH',
                            "amount": amount,
                            "value": value,
                            "price_per_unit": (value / amount),
                            "exchange": "GEMINI"
                        })
                # BTC
                elif row_cols[SYMBOL] == BTC:
                    amount = gemini_asset_to_float(row_cols[BTC_AMT])
                    if row_cols[TYPE] == taxable_terms[0]:
                        buys.append({
                            "timestamp": timestamp,
                            "asset": 'BTC',
                            "amount": amount,
                            "value": value,
                            "price_per_unit": (value / amount),
                            "exchange": "GEMINI"
                        })
                    elif row_cols[TYPE] == taxable_terms[1]:
                        sells.append({
                            "timestamp": timestamp,
                            "asset": 'BTC',
                            "amount": amount,
                            "value": value,
                            "price_per_unit": (value / amount),
                            "exchange": "GEMINI"
                        })

    return buys, sells


def gemini_amount_to_float(amount):
    if amount[0] == '(':
        return float(amount[2:-1].replace(",", ""))
    elif amount[0] == '$':
        return float(amount[1:].replace(",", ""))
    else:
        raise TypeError("Not a gemini amount: Form ($1.00) or $1.00")

def gemini_asset_to_float(asset_amt):
    if asset_amt[0] == '(':
        return float(asset_amt[1:-5].replace(",", ""))
    else:
        return float(asset_amt[0:-4].replace(",", ""))

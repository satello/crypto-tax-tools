from utils.timestamps import sort_list_by_timestamp

seconds_per_year = 60 * 60 * 24 * 365 # 60 sec * 60 min * 24 hours * 365 days

# SORT BY ASSET TYPE BEFORE
def FIFO(buys, sells, asset):
    # sort and reverse list so first in is at buys[-1]
    sort_list_by_timestamp(buys, True)
    # do the same for the sells
    sort_list_by_timestamp(sells, True)

    short_term_events = []
    long_term_events = []

    while (len(sells) > 0):
        if (len(buys) == 0):
            raise RuntimeError("There aren't enough buys to cover the sells")
        # pop off the next buy and sell
        sell_tx = sells.pop()
        next_buy = buys.pop()
        # print(next_buy)
        # print(sell_tx)
        if (next_buy["timestamp"] > sell_tx["timestamp"]):
            raise RuntimeError("There wasn't enough assets on %s to cover sell", sell_tx["timestamp"])

        # if the buy can cover the sell use the buy as the cost basis
        if (next_buy["amount"] >= sell_tx["amount"]):
            cost_basis = next_buy["price_per_unit"] * sell_tx["amount"]
            # add remaining buy back to array
            if sell_tx["amount"] < next_buy["amount"]:
                remaining_buy = next_buy.copy()
                remaining_buy["amount"] -= sell_tx["amount"]
                remaining_buy["value"] -= next_buy["price_per_unit"] * sell_tx["amount"]
                buys.append(remaining_buy)

            tx = {
                "buy_date": next_buy["timestamp"],
                "sell_date": sell_tx["timestamp"],
                "amount": sell_tx["amount"],
                "cost_basis": cost_basis,
                "asset": asset,
                "sell_value": sell_tx["value"]
            }
            # long term capital gains
            if (sell_tx["timestamp"] - next_buy["timestamp"]).seconds > seconds_per_year:
                long_term_events.append(tx)
            else:
                short_term_events.append(tx)
        # this buy alone can't cover
        else:
            cost_basis = next_buy["price_per_unit"] * next_buy["amount"]

            remaining_sell = sell_tx.copy()
            remaining_sell["amount"] -= next_buy["amount"]
            remaining_sell["value"] -= remaining_sell["price_per_unit"] * next_buy["amount"]
            sells.append(remaining_sell)

            tx = {
                "buy_date": next_buy["timestamp"],
                "sell_date": sell_tx["timestamp"],
                "amount": next_buy["amount"],
                "cost_basis": cost_basis,
                "asset": asset,
                "sell_value": sell_tx["price_per_unit"] * next_buy["amount"]
            }
            # long term capital gains
            if (sell_tx["timestamp"] - next_buy["timestamp"]).seconds > seconds_per_year:
                long_term_events.append(tx)
            else:
                short_term_events.append(tx)

    # returns short term, long term, and the remaining buys (you remaining portfolio. Good to know for future tax seasons)
    return short_term_events, long_term_events, buys

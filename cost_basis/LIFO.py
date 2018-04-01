from utils.timestamps import sort_list_by_timestamp

seconds_per_year = 60 * 60 * 24 * 365 # 60 sec * 60 min * 24 hours * 365 days

# SORT BY ASSET TYPE BEFORE
def LIFO(buys, sells, asset):
    # sort and reverse list so last in is at buys[-1]
    sort_list_by_timestamp(buys, True)
    # do the same for the sells
    sort_list_by_timestamp(sells, True)

    short_term_events = []
    long_term_events = []
    active_buys = []
    while(len(sells) > 0):
        current_sell = sells.pop()

        if (len(buys) > 0):
            # populate active_buys
            test_buy = buys.pop()
            while(current_sell["timestamp"] > test_buy["timestamp"]):
                active_buys.append(test_buy)
                if len(buys) == 0:
                    test_buy = None
                    break
                test_buy = buys.pop()

            # add last buy back into buy list
            if test_buy:
                buys.append(test_buy)

        next_buy = active_buys.pop()
        if not next_buy:
            raise RuntimeError("There are not enough buys to clear the sells")
        # if the buy can cover the sell use the buy as the cost basis
        if (next_buy["amount"] >= current_sell["amount"]):
            cost_basis = next_buy["price_per_unit"] * current_sell["amount"]
            # add remaining buy back to array
            if current_sell["amount"] < next_buy["amount"]:
                remaining_buy = next_buy.copy()
                remaining_buy["amount"] -= current_sell["amount"]
                remaining_buy["value"] -= next_buy["price_per_unit"] * current_sell["amount"]
                active_buys.append(remaining_buy)

            tx = {
                "buy_date": next_buy["timestamp"],
                "sell_date": current_sell["timestamp"],
                "amount": current_sell["amount"],
                "cost_basis": cost_basis,
                "asset": asset,
                "sell_value": current_sell["value"]
            }
            # long term capital gains
            if (current_sell["timestamp"] - next_buy["timestamp"]).seconds > seconds_per_year:
                long_term_events.append(tx)
            else:
                short_term_events.append(tx)
        # this buy alone can't cover
        else:
            cost_basis = next_buy["price_per_unit"] * next_buy["amount"]

            remaining_sell = current_sell.copy()
            remaining_sell["amount"] -= next_buy["amount"]
            remaining_sell["value"] -= remaining_sell["price_per_unit"] * next_buy["amount"]
            sells.append(remaining_sell)

            tx = {
                "buy_date": next_buy["timestamp"],
                "sell_date": current_sell["timestamp"],
                "amount": next_buy["amount"],
                "cost_basis": cost_basis,
                "asset": asset,
                "sell_value": current_sell["price_per_unit"] * next_buy["amount"]
            }
            # long term capital gains
            if (current_sell["timestamp"] - next_buy["timestamp"]).seconds > seconds_per_year:
                long_term_events.append(tx)
            else:
                short_term_events.append(tx)

    remaining_buys = buys + active_buys
    sort_list_by_timestamp(remaining_buys)
    # returns short term, long term, and the remaining buys (you remaining portfolio. Good to know for future tax seasons)
    return short_term_events, long_term_events, remaining_buys

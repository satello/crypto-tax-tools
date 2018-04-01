import csv
import sys
from parsers.parse_gdax_csv import parse_gdax
from parsers.parse_gemini_csv import parse_gemini
from utils.timestamps import sort_list_by_timestamp
from cost_basis.FIFO import FIFO
from cost_basis.LIFO import LIFO
from utils.reporting import report_asset_movement, report_asset_cost_basis

def FIFO_for_asset(buys, sells, asset):
    asset_short_term, btc_long_term, remaining_portfolio = FIFO(buys, sells, asset)

    report_asset_cost_basis(asset_short_term, '%s_short_term_FIFO.csv' % asset)
    report_asset_cost_basis(btc_long_term, '%s_long_term_FIFO.csv' % asset)
    report_asset_movement(remaining_portfolio, '%s_remianing_portfolio_after_FIFO.csv' % asset)

    print("FIFO")
    total_short_term_liability = sum(map(lambda x: x["sell_value"], asset_short_term)) - sum(map(lambda y: y["cost_basis"], asset_short_term))
    print("%s short term liability: %s" % (asset, total_short_term_liability))
    total_long_term_liability = sum(map(lambda x: x["sell_value"], btc_long_term)) - sum(map(lambda y: y["cost_basis"], btc_long_term))
    print("%s long term liability: %s" % (asset, total_long_term_liability))

def LIFO_for_asset(buys, sells, asset):
    asset_short_term, btc_long_term, remaining_portfolio = LIFO(buys, sells, asset)

    report_asset_cost_basis(asset_short_term, '%s_short_term_LIFO.csv' % asset)
    report_asset_cost_basis(btc_long_term, '%s_long_term_LIFO.csv' % asset)
    report_asset_movement(remaining_portfolio, '%s_remianing_portfolio_after_LIFO.csv' % asset)

    print("LIFO")
    total_short_term_liability = sum(map(lambda x: x["sell_value"], asset_short_term)) - sum(map(lambda y: y["cost_basis"], asset_short_term))
    print("%s short term liability: %s" % (asset, total_short_term_liability))
    total_long_term_liability = sum(map(lambda x: x["sell_value"], btc_long_term)) - sum(map(lambda y: y["cost_basis"], btc_long_term))
    print("%s long term liability: %s" % (asset, total_long_term_liability))

def main(gdax_file, gemini_file):
    gdax_buys, gdax_sells = parse_gdax(gdax_file)
    gemini_buys, gemini_sells = parse_gemini(gemini_file)
    all_buys = gdax_buys + gemini_buys
    all_sells = gdax_sells + gemini_sells

    sort_list_by_timestamp(all_buys)
    sort_list_by_timestamp(all_sells)

    report_asset_movement(all_buys, 'all_buys.csv')
    report_asset_movement(all_sells, 'all_sells.csv')

    btc_buys = filter(lambda x: x['asset'] == 'BTC', all_buys)
    btc_sells = filter(lambda x: x['asset'] == 'BTC', all_sells)
    FIFO_for_asset(list(btc_buys), list(btc_sells), 'BTC')
    LIFO_for_asset(list(btc_buys), list(btc_sells), 'BTC')

    eth_buys = filter(lambda x: x['asset'] == 'ETH', all_buys)
    eth_sells = filter(lambda x: x['asset'] == 'ETH', all_sells)
    FIFO_for_asset(list(eth_buys), list(eth_sells), 'ETH')
    LIFO_for_asset(list(eth_buys), list(eth_sells), 'ETH')

    ltc_buys = filter(lambda x: x['asset'] == 'LTC', all_buys)
    ltc_sells = filter(lambda x: x['asset'] == 'LTC', all_sells)
    FIFO_for_asset(list(ltc_buys), list(ltc_sells), 'LTC')
    LIFO_for_asset(list(ltc_buys), list(ltc_sells), 'LTC')

if __name__ == '__main__':
    gdax_file = './csv/gdax.csv'
    gemini_file = './csv/gemini.csv'
    if len(sys.argv) > 1:
        gdax_file = sys.argv[1]
    if len(sys.argv) > 2:
        gemini_file = sys.argv[2]

    main(gdax_file, gemini_file)

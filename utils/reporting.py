import csv

BASE_REPORT_DIR = './reports/'

def report_asset_movement(asset_movement_list, file_name):
    asset_movement_output_csv = open(BASE_REPORT_DIR + file_name, 'w')
    asset_movement_wr = csv.writer(asset_movement_output_csv, quoting=csv.QUOTE_ALL)

    asset_movement_headers = ["Timestamp", "Asset", "Amount", "Value (USD)", "Price Per Unit", "Exchange"]
    asset_movement_wr.writerow(asset_movement_headers)
    for line in asset_movement_list:
        asset_movement_wr.writerow([line["timestamp"], line["asset"], line["amount"], line["value"], line["price_per_unit"], line["exchange"]])

def report_asset_cost_basis(close_basis_result, file_name):
    asset_trades = open(BASE_REPORT_DIR + file_name, 'w')
    asset_trades_wr = csv.writer(asset_trades, quoting=csv.QUOTE_ALL)
    asset_trades_wr.writerow(["Buy Date", "Sell Date", "Asset", "Amount", "Cost Basis", "Sell Value", "Taxable Amount"])
    total_amt = 0
    total_cb = 0
    total_sv = 0
    total_tx = 0
    for trade in close_basis_result:
        total_amt += trade["amount"]
        total_cb += trade["cost_basis"]
        total_sv += trade["sell_value"]
        total_tx += (trade["sell_value"] - trade["cost_basis"])
        asset_trades_wr.writerow([trade["buy_date"], trade["sell_date"], trade["asset"], trade["amount"], trade["cost_basis"], trade["sell_value"], trade["sell_value"]-trade["cost_basis"]])
    asset_trades_wr.writerow(["TOTALS",None,None,total_amt,total_cb,total_sv,total_tx])

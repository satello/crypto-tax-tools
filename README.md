# Crypto Taxes Helper (United States)
For `python 2.7`

These are some python scripts I wrote to help me figure out my capital gains
obligations. It generates a report for all your buys, sells, buy/sell per asset amongst
BTC, ETH and LTC and also a report on the cost basis/tax obligations using FIFO.

(NOTE: Other cost basis tools WIP. LIFO should be done soon. Might try to make an optimized tx picker. Not totally sure if you are allowed to pick and choose like that though since at least I wasn't picking and choosing my UTXO's. I would also like to do a full on UTXO tracker but that sounds hard and taxes are due soon).

### Exchanges

Currently support parsing the trade csv downloaded from:

- GDAX
- Gemini


### Basic Usage

1) download your .csv reports from your exchanges that shows all of your yearly trading activity.
2) create a directory `reports` for your reports to be generated in
3)
```
python generate_reports.py <gdax.csv> <gemini.csv>
```
4) You should have lots of reports generated in your reports folder.

### Good to Know's

1) I just made this for myself. I don't know that your csv's will be the same format as mine.
2) If you have Gemini but not GDAX or vice versa you are going to have to hack it up to skip
one or the other. Could also just pass an empty csv for the one you are missing. If you have a different exchange why not write a parser for it and make a PR :)
3) GDAX market orders usually go through as a million little buys/sells which all show up on your csv.
I thought this would be a pain in the ass for both myself and for the IRS so I have it mashed together
tx's that are within 5 seconds of each other so it shows up as 1 trade per asset in that 5 second span. I don't do any arbitrage trading, algorithmic trading or otherwise trading via an API. Therefore that 5 second threshold works for me. It might not for you. Or maybe you want to report all those little trades separately. Up to you. If you need something different hack up `parsers/parse_gdax_csv.py`.
4) I definitely don't guarantee this is accurate. Nobody has audited this code. I have barely audited the reports it spits out (but from the simple math I have done by hand they look solid). So use it to help you sort your shit out but I wouldn't straight turn in what this spits out to the IRS without a good look over.
5) I just remembered something I was going to put in but forgot. It would be nice to pass a 3rd arg that is miscellaneous buys and sells from other sources as well. I will probably put that in soon but just note that if you don't include all of the assets you own the cost basis picking is going to be off and that could cause you issues in future tax seasons.

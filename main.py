import urllib.request
import json
import csv


# gets the price data from Coindesk BTC price API
def price_getter(url):
    with urllib.request.urlopen(url) as page:
        response = json.loads(page.read().decode())
        price_history = response["bpi"]
    return price_history


btc_price_usd = "https://api.coindesk.com/v1/bpi/historical/close.json"
btc_price_eur = "https://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR"

print(price_getter(btc_price_usd))

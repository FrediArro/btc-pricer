import os
import urllib.request
import json
import csv


# gets the price data from Coindesk BTC price API
def price_getter(url):
    with urllib.request.urlopen(url) as page:
        response = json.loads(page.read().decode())
        price_history = response["bpi"]
    return price_history


# writes price info to CSV local CSV file
def price_to_csv(price_info):
    # checks if the file already exist and if so, then deletes it
    # to not have any old/wrong info in the file.
    file_name = "price_history.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["date", "price"])
        for key, value in price_info.items():
            writer.writerow([key, value])

btc_price_usd = "https://api.coindesk.com/v1/bpi/historical/close.json"
btc_price_eur = "https://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR"

price_data = price_getter(btc_price_usd)
price_to_csv(price_data)

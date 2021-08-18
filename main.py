import os
import urllib.request
import json
import csv
import matplotlib.pyplot as plt


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


def send_csv():
    return ""


def data_to_plot(data):
    dates = []
    prices = []
    for key in data:
        dates.append(key[5:])
        prices.append(round(data[key], 2))
    max_price = max(prices)
    max_date_pos = prices.index(max_price)
    max_date = dates[max_date_pos]
    min_price = min(prices)
    min_date_pos = prices.index(min_price)
    min_date = dates[min_date_pos]
    # https://stackoverflow.com/questions/43374920/how-to-automatically-annotate-maximum-value-in-pyplot
    fig = plt.figure()
    ax = fig.add_subplot()
    price_line = ax.plot(dates, prices)
    ax.grid(color="gray", linestyle=":", linewidth=1)
    ax.annotate(max_price, xy=(max_date, max_price), xytext=(max_date, max_price+200))
    ax.annotate(min_price, xy=(min_date, min_price), xytext=(min_date, min_price-1000))
    ax.set_ylim(min_price-2000, max_price+2000)
    plt.title("BTC price last 31 days")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.ylabel("Price €")
    plt.show()


btc_price_usd = "https://api.coindesk.com/v1/bpi/historical/close.json"
btc_price_eur = "https://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR"

price_data = price_getter(btc_price_usd)
price_to_csv(price_data)
data_to_plot(price_data)

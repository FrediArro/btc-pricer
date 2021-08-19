import urllib.request
import json
import os
import csv
import matplotlib.pyplot as plt
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# price_getter(url) - gets the price data from Coindesk BTC price API
# url - Coindesk API to get the last 31 days price of BTC
def price_getter(url):
    with urllib.request.urlopen(url) as page:
        response = json.loads(page.read().decode())
        # price history is "bpi" key value
        price_history = response["bpi"]
    return price_history


# prices_to_csv(price_info) - writes price info to CSV local CSV file
# price_info - dictionary where key is the date and value is the BTC price on that date
def price_to_csv(price_info):
    # checks if the file already exist and if so, then deletes it
    # to not have any old/wrong info in the file.
    file_name = "price_history.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
    # opens/creates the file
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # writes the header to the file
        writer.writerow(["date", "price"])
        # writes the date and price to the file
        for key, value in price_info.items():
            writer.writerow([key, value])


# data_to_plot(data) - plots the the BTC price to interactive plot with matplotlib
# arg data - dictionary where key is the date and value is the BTC price on that date
def data_to_plot(data):
    dates = []
    prices = []
    # fills the dates and prices lists with data
    for key in data:
        dates.append(key[5:])
        prices.append(round(data[key], 2))
    # maximum and minimum price are found (and when they occurred)
    max_price = max(prices)
    max_date_pos = prices.index(max_price)
    max_date = dates[max_date_pos]
    min_price = min(prices)
    min_date_pos = prices.index(min_price)
    min_date = dates[min_date_pos]
    # figure is created
    fig = plt.figure()
    ax = fig.add_subplot()
    # mrice linegraph is plotted
    ax.plot(dates, prices)
    # adds gridlines to plot for better readability
    ax.grid(color="gray", linestyle=":", linewidth=1)
    # adding the min and max price to the plot
    # code referenced from:
    # https://stackoverflow.com/questions/43374920/how-to-automatically-annotate-maximum-value-in-pyplot
    ax.annotate("$" + str(max_price), xy=(max_date, max_price), xytext=(max_date, max_price + 200), color="green")
    ax.annotate("$" + str(min_price), xy=(min_date, min_price), xytext=(min_date, min_price - 1000), color="red")
    ax.set_ylim(min_price - 2000, max_price + 2000)
    # adding information about the axis
    plt.title("BTC price last 31 days in USD")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.ylabel("Price $")
    # showing the plot
    plt.show()


# need to enable access for less secure apps from https://www.google.com/settings/security/lesssecureapps
# https://www.google.com/settings/security/lesssecureapps
# https://realpython.com/python-send-email/
# send_email() - Sends an email from default or users SMTP server
def send_email():
    # gets smtp server address, user, password, sender's email address and receiver's email address
    smtp_server, port, user_name, password, sender_email, receiver_email = user_credentials()

    # email info: subject, sender, recipient, body
    message = MIMEMultipart()
    message["Subject"] = "Last 31 days BTC price report"
    message["From"] = sender_email
    message["To"] = receiver_email
    body = """
     Hello!
     
     I am a Python script, that sends you the BTC price over the last 31 days.
     That is all what I what I do.
     Thank you for your attention.
     
     Best regards,
     Python (not the snake)
     """
    # body is attached to the message
    message.attach(MIMEText(body, "plain"))
    file_name = "price_history.csv"
    # price report file is opened and attached to the file
    with open(file_name, "rb") as file:
        message.attach(MIMEApplication(file.read(), Name="price_history.csv"))
    context = ssl.create_default_context()
    # tries to login in to the server and send the email
    done = False
    while not done:
        try:
            # connecting to the server
            server = smtplib.SMTP_SSL(smtp_server, port, context=context)
            # logging in to the server
            server.login(user_name, password)
            # sending the email
            server.sendmail(message["From"], message["To"], message.as_string())
            print("""  
                    __________________
            -----  |\                /|
              ---  | \  BTC prices  / |
             ----  | /\____________/\ | 
           ------  |/                \|
                   |__________________|
                       """)
            print("\nReport sent!")
            server.close()
            done = True
        # if the process fails the error is printed out and the process starts over
        except Exception as e:
            print("")
            print("-----------------------------------------------------------------------------")
            print(e)
            print("-----------------------------------------------------------------------------")
            print("")
            send_email()


# user_credentials() - get the information about the email sending (if the user wants to user default or personal
# SMTP server
# gets smtp server address, user, password, sender's email address and receiver's email address
def user_credentials():
    print("Would you like to use your personal SMTP server or the default one?")
    print("NB!")
    print("If you are using gmail you need to ")
    print("enable access for less secure apps from https://www.google.com/settings/security/lesssecureapps")
    # if-else clause to use a default sender e-mail address
    # user_preference = input("P for Personal D for Default: ")
    # if user_preference.lower() == "d":
    #    # throwaway gmail account for running the script
    #    smtp_server = for example "smtp.gmail.com"
    #    port = for gmail 465
    #    user_name = e-mail address
    #    password = password
    #    sender_email = user_name
    # else:
    smtp_server = input("Enter the SMTP server url, where the email will be sent (gmail uses smtp.gmail.com): ")
    port = input("Enter the smtp server port (gmail uses 465): ")
    user_name = input("Enter the smtp server user (gmail uses the gmail address): ")
    password = input("Enter the smtp server user password: ")
    sender_email = input("Enter the sender email address: ")
    # The program asks the user to enter the email address of the recipient
    receiver_email = input("Enter the receiver email address: ")
    return smtp_server, port, user_name, password, sender_email, receiver_email


# btc_price_url - Coindesk API to get the last 31 days price of BTC
btc_price_url = "https://api.coindesk.com/v1/bpi/historical/close.json"

price_data = price_getter(btc_price_url)
price_to_csv(price_data)
data_to_plot(price_data)
send_email()

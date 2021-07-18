###IMPORTS###
import requests as rq
from bs4 import BeautifulSoup as bs
import json
import smtplib
import os
from datetime import datetime

###ATRIBUTES###
global data

###EXTRACT DATA###
data_file_path = os.path.dirname(os.path.realpath(__file__))
with open(data_file_path+"/data.json", "r") as data_file:
    data = json.load(data_file)

# Yahoo finance url
base_url = 'https://es.finance.yahoo.com/quote/ticker?p=ticker'


def get_price(url):
    """
    Returns the current price of a company given its yahoo finance url
    """
    r = rq.get(url)
    soup = bs(r.text, "lxml")  # might be lxml
    price = soup.find_all('div',
                          {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    return price


def check_prices(watchlist):
    """
    Returns a list of tickers whose prices are above our target price
    """
    on_target = []
    # Watchlist loop (all tickers in the data file)
    for ticker, target in data["Watchlist"].items():
        url = base_url.replace("ticker", ticker)
        price = float(get_price(url).replace(".", "").replace(",", "."))
        # If the price is above the target, we will send it to the email
        # and write the info in the registry.json file
        if price > target:
            on_target.append(ticker)
            print(ticker)
            on_target_info = {
                "ticker": ticker,
                "target_price": target,
                "on_target_date": str(datetime.now()),
                "yahoo_finance_link": url
            }
            with open(data_file_path+"/registry.json") as registry_file:
                new_registry_file = json.load(registry_file)
                new_registry_file["On_target_stocks"].append(on_target_info)

            with open(data_file_path+"/registry.json", 'w') as registry_file:
                json.dump(new_registry_file, registry_file, indent=4)

    return on_target


def send_email(ticker_list):
    """
    Sends email from adress in data file to other adress selected
    The mail format is the following:
    Subject: STOCK NOTIFY
    Content: text + tickers in taget + links of the tickers in yahoo finance
    """
    # Get email atributes
    sender_email = data["email"]["sender_email"]
    rec_email = data["email"]["rec_email"]
    password = data["email"]["password"]
    # Set the message content
    message = "Subject: STOCK NOTIFY\n\nSome stocks have reached target price!\n\n"
    for ticker in ticker_list:
        message += 'Tiker: {} -> Link: {}\n'.format(
            ticker, base_url.replace("ticker", ticker))
    # Setup the server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Introduce your mailing info
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, rec_email, message)
    server.quit()


def main():
    on_target = check_prices(data["Watchlist"])
    send_email(on_target) if len(on_target) > 0 else exit()
    # Remove from datafile the tickers on target
    for ticker in on_target:
        del data["Watchlist"][ticker]

    with open(data_file_path+"/data.json", 'w') as data_file:
        json.dump(data, data_file, indent=4)


if __name__ == "__main__":
    main()


from bs4 import BeautifulSoup
import requests
from yahoo_fin import options
import csv
from yahoo_fin import stock_info as si
import numpy as np

#Getting all option expiration dates of a stock
nflx_dates = options.get_expiration_dates("nflx")

#Writing information to new file (eventually do this every time a new stock is added by user)
with open('nflx.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(nflx_dates)

#Creates a list of all DOW tickers
dow_tickers = si.tickers_dow()

#Creates a list of all NASDAQ tickers
nasdaq_tickers = si.tickers_nasdaq()

#Creates a list of all S&P500 tickers
sp500_tickers = si.tickers_sp500()

all_major_stocks_tickers = []
for x in dow_tickers:
    all_major_stocks_tickers.append(x)

for x in nasdaq_tickers:
    all_major_stocks_tickers.append(x)

for x in sp500_tickers:
    all_major_stocks_tickers.append(x)

print(all_major_stocks_tickers)

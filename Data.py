from Linked_List import Linked_List
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
import yfinance as yf
from pandas import DataFrame
import requests
from pyllist import sllist


class Stock:
    def __init__(self, ticker):
        self.ticker = None
        self.earnings = None
        self.live_price = None
        self.historical_data_1 = None
        self.historical_data_3 = None
        self.sma_3_month = None
        self.ema_3_month = None
        self.full_data = None
        self.day_data = None
        self.ticker = ticker

    def __str__(self):
        return self.ticker

    def get_stock(self):
        self.live_price = si.get_live_price(self.ticker)
        return self.live_price

    def historical_data(self, ticker):
        self.historical_data_3 = ticker.history(period="3mo")
        self.historical_data_3 = self.historical_data_3.drop(columns=["Dividends", "Stock Splits"])
        self.full_data = self.historical_data_3
        self.full_data[" EMA 3 Month "] = self.historical_data_3.ewm(span=64)['Close'].mean().fillna('-')
        self.full_data[" SMA 3 Month "] = self.historical_data_3.rolling(window=64)['Close'].mean().fillna('-')
        self.full_data[" EMA 1 Month "] = self.historical_data_3.ewm(span=22)['Close'].mean().fillna('-')
        self.full_data[" SMA 1 Month "] = self.historical_data_3.rolling(window=22)['Close'].mean().fillna('-')
        self.full_data[" EMA 1 Week "] = self.historical_data_3.ewm(span=5)['Close'].mean().fillna('-')
        self.full_data[" SMA 1 Week"] = self.historical_data_3.rolling(window=5)['Close'].mean().fillna('-')
        self.day_data = self.full_data.tail(1)
        self.day_data.insert(0, 'Ticker', self.ticker)

        return self.day_data

class DataCollection:
    def __init__(self, portfolio):
        self.tickers = None
        self.frame = DataFrame
        self.portfolio = portfolio
        self.max_trade = self.portfolio//20
        self.stockPrice = 0

    def list_to_frame(self):
        self.tickers = si.tickers_sp500()
        list = []
        for val in range(len(self.tickers)):
            z = self.tickers[val]

         #token would be BKB.B but neeeded to be BKB-B and replace method wasn't working so hard coded it
            if "." in z:
                q = ""
                for i in z:
                    if i == ".":
                        i = "-"
                    q += i
                    z = q
            stock = Stock(z)
            price = stock.get_stock()
            if price < self.max_trade:
                ticker = yf.Ticker(z)
                data = stock.historical_data(ticker)
                list.extend(data.values.tolist())

        self.frame = DataFrame(list, columns=['Ticker','Open', 'High','Low','Close', 'Volume', 'EMA 3 Month', 'SMA 3 Month',
                                              'EMA 1 Month', 'SMA 1 Month','EMA 1 Week', 'SMA 1 Week'])
        return self.frame


    # def data_to_stocks(self):
    #     stocks = DataFrame()
    #     for ind in self.frame.index:
pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_columns", 12)
a = DataCollection(200) # change this for diff values :p
print(a.list_to_frame())


















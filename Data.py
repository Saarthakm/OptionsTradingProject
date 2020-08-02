from datetime import datetime
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
from pandas import DataFrame
import requests
from pyllist import sllist
from dateutil.relativedelta import relativedelta


class Stock:
    def __init__(self, ticker):
        self.ticker = None
        self.earnings = None
        self.live_price = None
        self.sma_3_month = None
        self.ema_3_month = None
        self.full_data = None
        self.day_data = DataFrame
        self.ticker = ticker
        self.current_date = self.weekend_check() + relativedelta(days=+1)
        self.date_3_months_ago = self.weekend_check()  + relativedelta(months=-3)
        self.column_list = ['ticker', 'open', 'high', 'low', 'close', 'volume']

    def __str__(self):
        return self.ticker

    def get_price(self):
        self.live_price = si.get_live_price(self.ticker)
        return self.live_price

    def weekend_check(self):
        date = datetime.date(datetime.now())
        if date.weekday() == 5:
            return datetime.date(datetime.now()) + relativedelta(days=-1)
        if date.weekday() == 6:
            return datetime.date(datetime.now()) + relativedelta(days=-2)
        return date

    def stock_day_data(self):


        self.full_data = si.get_data(self.ticker, self.date_3_months_ago, self.current_date)
        self.full_data = self.full_data.drop(columns=["adjclose"])
        self.full_data = self.full_data.reindex(columns=self.column_list)
        self.full_data[" EMA 3 Month "] = self.full_data.ewm(span=64)['close'].mean().fillna('-')
        self.full_data[" SMA 3 Month "] = self.full_data.rolling(window=64)['close'].mean().fillna('-')
        self.full_data[" EMA 1 Month "] = self.full_data.ewm(span=22)['close'].mean().fillna('-')
        self.full_data[" SMA 1 Month "] = self.full_data.rolling(window=22)['close'].mean().fillna('-')
        self.full_data[" EMA 1 Week "] = self.full_data.ewm(span=5)['close'].mean().fillna('-')
        self.full_data[" SMA 1 Week"] = self.full_data.rolling(window=5)['close'].mean().fillna('-')
        self.day_data = self.full_data.tail(1)
        return self.day_data

    def historical_data(self, period):
        call_back_date = self.current_date + relativedelta(days=-period)
        self.full_data = si.get_data(self.ticker, call_back_date, self.current_date)
        self.full_data = self.full_data.drop(columns=["adjclose"])
        self.full_data = self.full_data.reindex(columns=self.column_list)
        return self.full_data


class DataCollection:
    def __init__(self, portfolio):
        self.tickers = None

        self.portfolio = portfolio
        self.max_trade = self.portfolio/20
        self.stockPrice = 0
        self.list = []
    def list_to_frame(self):
        self.tickers = si.tickers_sp500()
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
            price = stock.get_price()


            if price < self.max_trade:
                # data = stock.day_data()
                self.list.append(z)

        return self.list

class OPAlgorithms:
    def __init__(self, list, portfolio):
        self.list = list
        self.strength = None
        self.threshhold = None
        self.portfolio = portfolio
        self.max_trade = portfolio/20  # maybe the one division matters :p
        self.cur_date_hist = self.weekend_check() + relativedelta(days=+1)
        self.cur_date = self.weekend_check()
        self.data = None
        self.stock_dict ={}
    def weekend_check(self):
        date = datetime.date(datetime.now())
        if date.weekday() ==5:
            return datetime.date(datetime.now()) +relativedelta(days=-1)
        if date.weekday() ==6:
            return datetime.date(datetime.now()) + relativedelta(days=-2)
        return date

    def sma(self, ticker, period_days):
        self.data = ticker.historical_data(period_days)
        self.data["Simple Moving Average"] = self.data['close'].rolling(window=period_days//2).mean().fillna('')
        self.data = self.data.tail(1)
        self.data = self.data.iloc[:, -1]
        self.data = float(self.data.to_string(index=False))
        return self.data

    def compare_sma(self, long_sma, short_sma):
        if long_sma<short_sma:
            return True
        else:
            return False

    def analyze_pruned_list(self):
        for val in range(len(self.list)):
            stock = Stock(self.list[val])
            self.stock_dict[self.list[val]] = self.compare_sma(self.sma(stock,21),self.sma(stock,13))
        return self.stock_dict




pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows",30)
b = DataCollection(200)
b = b.list_to_frame()
# b= DataFrame
a = OPAlgorithms(b, 200)
print(a.analyze_pruned_list())
# ua = Stock('AMD')
# ub = Stock('COTY')
# uc = Stock('UA')
# stocks = [ua,ub,uc]
# stockies = ["AMD","UA","COTY"]
# c = OPAlgorithms(stockies, 200)
# print(c.analyze_pruned_list())
# print(a.sma(ua ,20).to_string)



















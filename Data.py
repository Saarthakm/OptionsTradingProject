from datetime import datetime
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
from pandas import DataFrame
import requests
from pyllist import sllist
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


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
        self.figures = {}

    def weekend_check(self):
        date = datetime.date(datetime.now())
        if date.weekday() ==5:
            return datetime.date(datetime.now()) +relativedelta(days=-1)
        if date.weekday() ==6:
            return datetime.date(datetime.now()) + relativedelta(days=-2)
        return date

    def sma(self, ticker, period_days, window):
        self.data = ticker.historical_data(period_days)
        self.data["Simple Moving Average"] = self.data['close'].rolling(window= window).mean().fillna('')
        self.data = self.data.tail(1)
        self.data = self.data.iloc[:, -1]
        self.data = float(self.data.to_string(index=False))
        return self.data
    def sma_full_data(self, ticker, period_days , window):
        self.data = ticker.historical_data(period_days+1000)
        self.data["Simple Moving Average " + str(window) +" days"] = self.data['close'].rolling(
            window= window).mean().fillna('')
        self.data = self.data.drop(columns=["open", "volume", "high", "low", "close"])

        return self.data
    def ewm_full_data(self,ticker,period_days,span):
        self.data = ticker.historical_data(period_days)
        self.data["EWA " + str(span) + " days"] = self.data.ewm(span=span)['close'].mean().fillna('-')
        self.data = self.data.drop(columns=["open", "volume", "high", "low", "close"])

        return self.data

    def volume_data(self,ticker,period_days):
        self.data = ticker.historical_data(period_days)
        self.data = self.data.drop(columns=["open", "high", "low", "close"])
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
    def macd(self, ticker):
        ewm_12 = self.ewm_full_data(ticker,26,12)
        ewm_26 = self.ewm_full_data(ticker,26,26)

        df = DataFrame

        df= np.subtract(ewm_12["EWA 12 days"], ewm_26["EWA 26 days"])
        # df = np.multiply(df, 100)
        print(ticker.ticker)
        print(df)


        return df

    def data_plot(self):

        for val in range(len(self.list)):
            stock = Stock(self.list[val])
            db = stock.historical_data(20)
            start_date= db.index.min()
            avg_long = self.sma_full_data(stock, 100, 50)
            avg_long = avg_long.truncate(before = start_date)

            avg_short = self.sma_full_data(stock, 100, 5)
            avg_short = avg_short.truncate(before = start_date)

            evm_short = self.ewm_full_data(stock,365,3)
            evm_short = evm_short.truncate(before=start_date)
            mac = self.macd(stock)
            mac = mac.truncate(before=start_date)
            volume = self.volume_data(stock,365)
            db = db.drop(columns=["open","volume","high", "low"])


            result = pd.concat([db,avg_long,avg_short,evm_short], axis = 1, join='outer')

            fig,(ax1,ax2) = plt.subplots(2,sharex = True)
            result.plot(ax =ax1)
            mac.plot(ax = ax2,label='MACD')
            # plt.plot(ax = ax2, y=0)
            ax1.set_title(stock.ticker)
            plt.legend(loc='best')
            plt.show()




pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows",100)
# b = DataCollection(200)
# b = b.list_to_frame()
#  b= DataFrame
# a = OPAlgorithms(b, 200)
# print(a.analyze_pruned_list)
# ua = Stock('HRC')
# ub = Stock('COTY')
uc = Stock('UA')
# stocks = [ua,ub,uc]
stockies = ["XPO","OPK","UMICY"]
c = OPAlgorithms(stockies, 200)
c.data_plot()
# print(a.sma(ua ,20).to_string)



















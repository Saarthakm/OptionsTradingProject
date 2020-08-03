from datetime import datetime
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
from pandas import DataFrame
import requests
from pyllist import sllist
from dateutil.relativedelta import relativedelta
# from py_vollib.black_scholes.greeks.analytical import
import matplotlib.pyplot as plt
import Stock as st

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
            stock = st.Stock(z)
            price = stock.get_price()

            if price < self.max_trade:
                # data = stock.day_data()
                self.list.append(z)

        return self.list

    def stock_create(self, tick):
        s = st.Stock(tick)
        return s


class data_indicators:
    def __init__(self, list, portfolio):
        self.list = list
        self.strength = None
        self.threshhold = None
        self.portfolio = portfolio
        self.max_trade = portfolio / 20  # maybe the one division matters :p
        self.cur_date_hist = self.weekend_check() + relativedelta(days=+1)
        self.cur_date = self.weekend_check()
        self.data = None
        self.stock_dict = {}
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

    def volumetric_sma(self, ticker, period, window):
        volume_data= self.volume_data(ticker, period)
        volume_data[str(window) + " day volumetric SMA"] = volume_data.rolling(window=window).mean().fillna('')
        volume_data = volume_data.drop(columns=["volume"])
        return volume_data

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
            stock = st.Stock(self.list[val])
            self.stock_dict[self.list[val]] = self.compare_sma(self.sma(stock, 21), self.sma(stock, 13))
        return self.stock_dict

    def macd(self, ticker):
        ewm_12 = self.ewm_full_data(ticker, 365, 12)  # change period to param probably
        ewm_26 = self.ewm_full_data(ticker, 365, 26)

        df = DataFrame

        df = np.subtract(ewm_12["EWA 12 days"], ewm_26["EWA 26 days"])
        # df = np.multiply(df, 100)
        print(ticker.ticker)
        print(df)
        return df

    def compute_rsi(self, ticker, timewindow):
        ticker = st.Stock(ticker)
        datum = ticker.historical_data(20)
        close = datum["close"]
        delta = close.diff(1).dropna()
        up_chg = 0 *delta
        down_chg = 0*delta
        up_chg[delta>0]=delta[delta>0]
        down_chg[delta < 0] = delta[delta<0]
        up_chg_avg = up_chg.ewm(span=timewindow).mean()
        down_chg_avg = down_chg.ewm(span=timewindow).mean()
        # up_chg_avg = up_chg.rolling(window=timewindow).mean()
        # down_chg_avg = down_chg.rolling(window=timewindow).mean()
        rs = abs(up_chg_avg/down_chg_avg)
        rsi = 100-(100/(1+rs))
        return rsi
    def volume_oscillator(self, ticker):
        df1 = self.volumetric_sma(ticker, 500, 28)
        df2 = self.volumetric_sma(ticker, 500, 14)
        df1=df1.drop(columns=["ticker"])
        df2= df2.drop(columns=["ticker"])
        df2["14 day volumetric SMA"] = pd.to_numeric(df2["14 day volumetric SMA"], errors='coerce')
        df1["28 day volumetric SMA"] = pd.to_numeric(df1["28 day volumetric SMA"], errors='coerce')
        df = DataFrame
        df = np.subtract(df2["14 day volumetric SMA"], df1["28 day volumetric SMA"])
        df = df.dropna()
        # df2 = df2.drop(columns=['ticker'])
        # d3 = pd.concat([df1, df2], axis=1, join='outer')
        # d3=d3.tail(1)
        # d3 = DataFrame
        # d3 = np.subtract(df2["14 day volumetric SMA"], df1["28 day volumetric SMA"])
        return df






pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows",100)
# b = DataCollection(200)
# b = b.list_to_frame()
#  b= DataFrame
# a = OPAlgorithms(b, 200)
# print(a.analyze_pruned_list)
# ua = Stock('HRC')
ub = st.Stock('AMD')
# uc = st.Stock('UA')
# stocks = [ua,ub,uc]
stockies = ["XPO", "OPK", "UMICY"]
x = data_indicators(stockies, 200)
print(x.volume_oscillator(ub))
# c = OPAlgorithms(stockies, 200)
# c.data_plot()
# print(a.sma(ua ,20).to_string)

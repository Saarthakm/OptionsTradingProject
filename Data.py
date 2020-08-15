from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from scipy import stats
from yahoo_fin import stock_info as si

import Stock as st
import list


class DataCollection:
    def __init__(self, portfolio):
        self.tickers = list.stock_list1

        self.portfolio = portfolio
        self.max_trade = self.portfolio / 20
        self.stockPrice = 0
        self.list = []

    # only use this if getting stock names from yahoo_fin, not alpacas
    def list_to_frame(self):

        for val in range(len(self.tickers)):
            z = self.tickers[val]
            try:
                # token would be BKB.B but neeeded to be BKB-B and replace method wasn't working so hard coded it
                if "." in z:
                    q = ""
                    for i in z:
                        if i == ".":
                            i = "-"
                        q += i
                        z = q
                stock = st.Stock(z)
                price = stock.get_price()
                print(val)
                if price < self.max_trade and price > 3:
                    # data = stock.day_data()
                    self.list.append(z)
            except AssertionError:
                print(z)
        return self.list


class data_indicators:
    def __init__(self, list, portfolio, ticker, period):
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
        self.ticker = ticker
        self.org_period = period
        self.period = period
        self.strength = 0

    # corrects day to most recent trading day if current day is weekend
    def weekend_check(self):
        date = datetime.date(datetime.now())
        if date.weekday() == 5:
            return datetime.date(datetime.now()) + relativedelta(days=-1)
        if date.weekday() == 6:
            return datetime.date(datetime.now()) + relativedelta(days=-2)
        return date

    # creates stock
    def stock_create(self, tick):
        s = st.Stock(tick)
        return s

    # returns sma for current day
    def sma(self, ticker, period_days, window):
        self.data = ticker.historical_data(period_days)
        self.data["Simple Moving Average"] = self.data['close'].rolling(window=window).mean().fillna('')
        self.data = self.data.tail(1)
        self.data = self.data.iloc[:, -1]
        self.data = float(self.data.to_string(index=False))
        return self.data

    # returns sma df for all days in period
    def sma_full_data(self, ticker, period_days, window):
        self.data = ticker.historical_data(period_days + 1000)
        self.data["Simple Moving Average " + str(window) + " days"] = self.data['close'].rolling(
            window=window).mean().fillna('')
        self.data = self.data.drop(columns=["open", "volume", "high", "low", "close"])
        return self.data

    # avg of volume
    def volumetric_sma(self, ticker, period, window):
        volume_data = self.volume_data(ticker, period)
        volume_data[str(window) + " day volumetric SMA"] = volume_data.rolling(window=window).mean().fillna('')
        volume_data = volume_data.drop(columns=["volume"])
        return volume_data

    # returns ewa for period and span
    def ewm_full_data(self, ticker, period_days, span):
        self.data = ticker.historical_data(period_days)
        self.data["EWA " + str(span) + " days"] = self.data.ewm(span=span)['close'].mean().fillna('-')
        self.data = self.data.drop(columns=["open", "volume", "high", "low", "close"])

        return self.data

    # returns last row as float for dataframe
    def dataframe_short_float(self, data):
        data = data.tail(1)
        data = data.iloc[:, -1]
        data = float(data.to_string(index=False))
        return data

    # returns volume data
    def volume_data(self, ticker, period_days):
        self.data = ticker.historical_data(period_days)
        self.data = self.data.drop(columns=["open", "high", "low", "close"])
        return self.data

    # calculates macd
    def macd(self, ticker):
        ewm_12 = self.ewm_full_data(ticker, self.period + 22, 10)  # change period to param probably
        ewm_26 = self.ewm_full_data(ticker, self.period + 22, 22)

        df = DataFrame

        df = np.subtract(ewm_12["EWA 10 days"], ewm_26["EWA 22 days"])
        # df = np.multiply(df, 100)

        return df

    # calculates rsi
    def compute_rsi(self, ticker, timewindow):
        ticker = st.Stock(ticker)
        datum = ticker.historical_data(365)
        close = datum["close"]
        delta = close.diff(1).dropna()
        up_chg = 0 * delta
        down_chg = 0 * delta
        up_chg[delta > 0] = delta[delta > 0]
        down_chg[delta < 0] = delta[delta < 0]
        # up_chg_avg = up_chg.ewm(span=timewindow).mean()
        # down_chg_avg = down_chg.ewm(span=timewindow).mean()
        up_chg_avg = up_chg.rolling(window=timewindow).mean()
        down_chg_avg = down_chg.rolling(window=timewindow).mean()
        rs = abs(up_chg_avg / down_chg_avg)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # calculates diff in volume
    def volume_oscillator(self, ticker):
        df1 = self.volumetric_sma(ticker, 500, 28)
        df2 = self.volumetric_sma(ticker, 500, 14)
        df1 = df1.drop(columns=["ticker"])
        df2 = df2.drop(columns=["ticker"])
        df2["14 day volumetric SMA"] = pd.to_numeric(df2["14 day volumetric SMA"], errors='coerce')
        df1["28 day volumetric SMA"] = pd.to_numeric(df1["28 day volumetric SMA"], errors='coerce')
        df = DataFrame
        df = np.subtract(df2["14 day volumetric SMA"], df1["28 day volumetric SMA"])
        # df = np.divide(df, df1["28 day volumetric SMA"])
        # df = np.multiply(df, 100)
        df = df.dropna()
        # df2 = df2.drop(columns=['ticker'])
        # d3 = pd.concat([df1, df2], axis=1, join='outer')
        # d3=d3.tail(1)
        # d3 = DataFrame
        # d3 = np.subtract(df2["14 day volumetric SMA"], df1["28 day volumetric SMA"])
        return df

    # calculates rate of change for volatility index
    def vix_roc(self, number_days):
        vix = st.Stock("^VIX")
        data = si.get_data("^VIX", self.cur_date + relativedelta(days=-(number_days + 22)),
                           self.cur_date + relativedelta(days=-number_days))
        data.drop(columns=["adjclose", "open", "low", "high", "volume"])
        data["VIX EMA"] = data.ewm(span=22)['close'].mean().fillna('-')
        data1 = si.get_data("^VIX", self.cur_date + relativedelta(days=-number_days), self.cur_date)
        data1.drop(columns=["adjclose", "open", "low", "high", "volume"])
        data1["VIX EMA"] = data1.ewm(span=22)['close'].mean().fillna('-')
        data1 = data1.tail(1)
        data1 = data1.iloc[:, -1]
        data1_float = float(data1.to_string(index=False))

        data = data.tail(1)
        data = data.iloc[:, -1]
        data_float = float(data.to_string(index=False))
        data2 = ((data1_float / data_float) - 1) * 100

        return data2

    # not sure why we made this, average of the vix rate of change
    def avg_vix_roc(self):
        list = []
        for i in range(22, 1, -1):
            list.append(self.vix_roc(i))

        df = DataFrame(list, columns=["AVG ROCS"])
        df["AVG"] = df.ewm(span=21)["AVG ROCS"].mean()
        df = df.tail(1)
        df = df.iloc[:, -1]
        df = float(df.to_string(index=False))
        return df

    # current version for buying
    def stock_check(self):
        buy = True
        try:

            index = self.org_period - self.period
            stock = self.stock_create(self.ticker)
            # price = si.get_live_price(self.ticker)
            data = stock.historical_data(self.org_period)
            data = data.drop(columns={'ticker', 'open', 'high', 'low', 'volume'})
            data = data.to_numpy()
            price = data[len(data) - 1]
            x = self.ewm_full_data(stock, self.org_period + 10, 10)
            x = x.drop(columns="ticker")
            # x = x.tail(1)
            # x = x.iloc[:, -1]
            x = x.to_numpy()
            # x = float(x.to_string(index=False))

            emw_price = x[len(x) - 1]

            diff = emw_price - price
            percent = (diff / emw_price) * 100
            macd = self.macd(stock)

            signal = macd.ewm(span=9).mean().fillna('-')

            m = (macd[len(macd) - 2] - macd[len(macd) - 1]) / (0 - 1)  # calculate slope of macd

            if m < 0:
                self.strength = percent * -1  # if slope negative, then invert our strength of stock
            else:
                self.strength = percent

            macd = macd.to_numpy()

            signal = signal.to_numpy()

            if len(macd) < 10:  # if days are missing from data
                buy = False
            else:
                if emw_price < price:  # possibly add hour data for more accurate
                    buy = False
                if macd[len(macd) - 1] < signal[len(signal) - 1]:  # maybe look into this more macd span. yer yeet!
                    buy = False
                if price > self.max_trade or price <= 1:  # "get rid of shitter penny stocks"
                    buy = False
        except AssertionError:  # stock is listed on alpacas but not yahoo
            print(self.ticker)
            buy = False

        except IndexError:  # day or more is missing from data
            print(self.ticker)
            buy = False
        return buy

    # returns dictionary with stocks that pass initial buy check
    # Value is strength number
    def dict_maker(self):  # Only run once per day until we get that op op poly data
        dict = {}
        i = 1
        for val in self.list:
            print(i)
            self.ticker = val
            if self.stock_check():
                dict[val] = float(self.strength)
            i += 1
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        return dict

    # Currently inverse of buying
    def sell_stock(self):
        if self.stock_check():
            return False
        else:
            return True


# format df outputs
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows", 100)

# testing stock check and eval strength numbers

# b = data_indicators(list.stock_list, 500, "UA", 30)
# print(b.dict_maker())
# stockies = []
# b = DataCollection(500)
# c = list.list_through_algo
#
# i = 1
# for val in c:
#     b = data_indicators(c, 500, val, 1)
#     try:
#         if b.stock_check():
#             stockies.append(val)
#         print(i)
#         i += 1
#     except AssertionError:
#         print(val)
#     except KeyError:
#         print(val)
# print(stockies)



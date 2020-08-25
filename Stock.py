from datetime import datetime
from yahoo_fin import stock_info as si
from pandas import DataFrame
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
        self.date_3_months_ago = self.weekend_check() + relativedelta(months=-3)
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
        self.full_data = self.full_data.dropna()
        self.full_data = self.full_data.reindex(columns=self.column_list)
        return self.full_data

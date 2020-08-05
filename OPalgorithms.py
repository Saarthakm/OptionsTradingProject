from Data import DataCollection as dc
from Data import data_indicators as di
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
from pandas import DataFrame
import Stock as st
import alpaca_trade_api as ap


class algorithm:

    def __init__(self, stock, price):
        self.stock = st.Stock(stock)
        self.price = price

    def stock_check(self):
        buy = True
        ema_10 = di.dataframe_short_float(di.ewm_full_data(self.stock, 10, 10))
        macd = di.macd(self.stock)
        signal = macd.ewm(span=9).mean().fillna('-')
        macd = di.dataframe_short_float(macd)
        signal = di.dataframe_short_float(signal)
        if ema_10 < self.price:
            buy = False
        if macd < signal:
            buy = False
        return buy

    def sell(self):
        if self.stock_check() == True:
            return False
        else:
            return True

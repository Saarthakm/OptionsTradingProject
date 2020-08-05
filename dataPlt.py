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

from Data import DataCollection as dc
from Data import data_indicators as di


class DataPlt:
    def __init__(self):
        self.stock_list = ["AMZN", "OPK", "UMICY"]

    def plot(self):
        for val in range(len(self.stock_list)):
            stock = dc(200)
            x = di(self.stock_list, 200)
            stock = dc.stock_create(stock, self.stock_list[val])
            db = stock.historical_data(365)
            start_date = db.index.min()
            avg_long = di.sma_full_data(stock, stock, 100, 50)
            avg_long = avg_long.truncate(before=start_date)

            avg_short = di.sma_full_data(stock, stock, 100, 5)
            avg_short = avg_short.truncate(before=start_date)

            evm_short = di.ewm_full_data(x, stock, 100, 3)
            evm_short = evm_short.truncate(before=start_date)
            mac = di.macd(x, stock)
            mac = mac.truncate(before=start_date)
            signal = mac.ewm(span=9).mean().fillna('-')
            volume = di.volume_data(x, stock, 365)
            db = db.drop(columns=["open", "volume", "high", "low"])

            result = pd.concat([db, avg_long, avg_short, evm_short], axis=1, join='outer')

            fig, (ax1, ax2) = plt.subplots(2, sharex=True)
            result.plot(ax=ax1)
            mac.plot(ax=ax2, label='MACD')
            signal.plot(ax=ax2, label ='Signal Line')
            # plt.plot(ax = ax2, y=0)
            ax1.set_title(stock.ticker)
            ax2.set_title('MACD and Signal')
            plt.legend(loc='best')
            plt.show()


if __name__ == '__main__':
    a = DataPlt()
    a.plot()

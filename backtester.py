from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from yahoo_fin import stock_info as si
import list
import Stock as st
from Data import data_indicators as di
import backtrader as bt


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        self.stock = st.Stock("GOOG")
        self.dt = self.stock.historical_data(30)
        list = []
        self.sell_count = 0
        self.buy_count = 0
        self.period = 30

    def next(self):
        list = []
        d = di(list, 500, val, self.period)
        print(val)
        self.period -= 1
        if d.stock_check():
            self.buy()
            self.buy_count += 1
            # print(str(self.buy_count) + "buy")
        elif d.sell_stock():
            while self.sell_count < self.buy_count:
                self.sell()
                self.sell_count += 1
                # print(self.sell_count)


# api error causes nones use try catch
for val in list.list_through_algo:
    hist_data = st.Stock(val).historical_data(30)
    hist_data = hist_data.drop(columns=["ticker"])
    hist_data = hist_data.rename(
        columns={'open': "Open", 'high': "High", 'low': "Low", 'close': "Close", 'volume': "Volume"})
    hist_data = hist_data.dropna()

    btest = Backtest(hist_data, SmaCross, trade_on_close=True, exclusive_orders=True)
    stats = btest.run()
    # print(stats)
    btest.plot()
# btest = Backtest(data, SmaCross,trade_on_close=True)

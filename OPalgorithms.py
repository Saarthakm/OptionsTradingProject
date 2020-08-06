from Data import DataCollection as dc
from Data import data_indicators as di
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
from pandas import DataFrame
import Stock as st
import alpaca_trade_api as ap
import list

class algorithm:

    def __init__(self, stock, price):
        self.stock = stock
        self.price = price

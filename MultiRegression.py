from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split



#This class pertains to multiple linear regression modeling, with ordinary least squares as the loss function. This class will handle
#data preprocessing, cross validation, train-test split, building loss visualizations, feature engineering. We will be experimenting with L1 and L2
#loss, aka ridge and lasso regression. The final output will be train and test accuracy on the model, as well as inputting a stock and predicting it's
#price daily, weekly, and monthly

class MultiLinearRegression:
    def __init__(self, ticker, startdate, enddate):
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate
        self.liveprice = None
        self.X_train = None
        self.Y_train = None
        self.X_test = None
        self.Y_test = None
        self.data = None


    def get_curr_price(self):
        self.live_price = si.get_live_price(self.ticker)
        return self.live_price

    def get_historic_data(ticker):
            self.data = si.get_data(ticker, start_date=self.startdate, end_date=self.enddate, index_as_date=False)
            return self.data

    def crossValidation(self):
        return 0

    def train_test_split(self):
        X = get_historic_data(self.ticker)
        temp = X
        X = X.drop('adjclose')
        Y = pd.Series(temp['adjclose'])
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, train_size = .9)
        return self.X_train, self.X_test, self.Y_train, self.Y_test


    def rmse(self, actual_y, predicted_y):
        return np.sqrt(np.mean((actual_y - predicted_y) ** 2))


    def customFeatureEngineering(self, self.X):
        df =

    def buildMultiRegModel(self, ticker):
        df = get_historic_data(ticker)
        regressor = linear_model.LinearRegression()

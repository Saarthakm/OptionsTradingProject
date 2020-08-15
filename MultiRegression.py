from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
from sklearn import metrics




#This class pertains to multiple linear regression modeling, with ordinary least squares as the loss function. This class will handle
#data preprocessing, cross validation, train-test split, building loss visualizations, feature engineering. We will be experimenting with L1 and L2
#loss, aka ridge and lasso regression. The final output will be train and test accuracy on the model, as well as inputting a stock and predicting it's
#price daily, weekly, and monthly

class MultiLinearRegression:
    def __init__(self, ticker, startdate, enddate):
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate
        self.liveprice = si.get_live_price(self.ticker)
        self.X_train = None
        self.Y_train = None
        self.X_test = None
        self.Y_test = None
        self.data = None
        self.predictions = None
        #all data of tomorrow except open price
        self.yesterdayData = None
        self.fittedRegressor = None
        self.tomorrowPredictedPrice = None


    def get_historic_data(self):
            self.data = si.get_data(self.ticker, start_date=self.startdate, end_date=self.enddate, index_as_date=False)
            temp = si.get_data(self.ticker, start_date=self.startdate, end_date=self.enddate, index_as_date=False)
            self.yesterdayData = temp.tail(1)
            self.yesterdayData = self.yesterdayData.drop(columns = ['adjclose', 'close', 'ticker'])
            self.yesterdayData = self.yesterdayData.drop(self.yesterdayData.columns[0], axis=1)
            self.data[['high', 'low', 'close', 'adjclose', 'volume', 'ticker']] = self.data[['high', 'low', 'close', 'adjclose', 'volume', 'ticker']].shift(1)
            self.data = self.data.tail(len(self.data) - 1)
            #DO THE YESTERDAYDATA STUFF LATER!!!!! DON'T FORGET!

            return self.data

    def crossValidation(self):
        return 0

    def train_test_split(self):
        X = self.get_historic_data()
        temp = X
        X = X.drop(columns = ['adjclose', 'close', 'ticker'])
        Y = pd.Series(temp['adjclose'])
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, train_size = .9)
        self.X_train = self.X_train.drop(self.X_train.columns[0], axis=1)
        self.X_test = self.X_test.drop(self.X_test.columns[0], axis=1)
        return self.X_train, self.X_test, self.Y_train, self.Y_test


    def rmse(self, actual_y, predicted_y):
        return np.sqrt(np.mean((actual_y - predicted_y) ** 2))


    def buildMultiRegModel(self):
        df = self.train_test_split()
        regressor = linear_model.LinearRegression()
        fittedReg = regressor.fit(self.X_train, self.Y_train)
        prediction = fittedReg.predict(self.X_test)
        self.predictions = prediction
        self.fittedRegressor = fittedReg
        return prediction

    def calculatePercentDiff(self):
        X = self.buildMultiRegModel()
        return np.average(((X - self.Y_test) / (self.Y_test)) * 100)

    def score(self):
        self.buildMultiRegModel()
        print("Model R^2: " + str(metrics.r2_score(self.Y_test, self.predictions)))

    def predictTomorrowsPrice(self):
        pred = self.fittedRegressor.predict(self.yesterdayData)
        self.tomorrowPredictedPrice = pred[0]
        print("Tomorrow, " + self.ticker.upper() + " share is predicted to be priced at: $" + str(pred[0]))
        print("Yesterday at close, " + self.ticker.upper() + " was trading at: $" + str(self.liveprice))
        print("")



AMD = MultiLinearRegression('amd', '12/1/2000', '8/14/2020')
AMD.get_historic_data()
AMD.train_test_split()
AMD.buildMultiRegModel()
AMD.predictTomorrowsPrice()

MSFT = MultiLinearRegression('msft', '12/1/2000', '8/14/2020')
MSFT.get_historic_data()
MSFT.train_test_split()
MSFT.buildMultiRegModel()
MSFT.predictTomorrowsPrice()

AMD = MultiLinearRegression('lyft', '12/1/2019', '8/14/2020')
AMD.get_historic_data()
AMD.train_test_split()
AMD.buildMultiRegModel()
AMD.predictTomorrowsPrice()

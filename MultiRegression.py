from yahoo_fin import stock_info as si
from sklearn import linear_model




#This class pertains to multiple linear regression modeling, with ordinary least squares as the loss function. This class will handle
#data preprocessing, cross validation, train-test split, building loss visualizations, feature engineering, 
class MultiLinearRegression:
    def __init__(self, ticker, startdate, enddate):
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate



    def get_historic_data(ticker):
            si.get_data(ticker, start_date='01/01/2010', end_date='07/31/2020', index_as_date = False)


    def buildMultiRegModel(ticker):
        df = get_historic_data(ticker)
        regressor = linear_model.LinearRegression()



    def crossValidation():

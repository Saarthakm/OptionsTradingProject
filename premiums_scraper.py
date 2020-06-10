import requests
from yahoo_fin import options
import csv
from yahoo_fin import stock_info as si
import pandas as pd

#Getting all option expiration dates of a stock
nflx_dates = options.get_expiration_dates("nflx")
nflx_calls = options.get_calls("nflx")

#Creates a list of all DOW tickers
dow_tickers = si.tickers_dow()

#Creates a list of all NASDAQ tickers
nasdaq_tickers = si.tickers_nasdaq()

#Creates a list of all S&P500 tickers
sp500_tickers = si.tickers_sp500()

all_major_stocks_tickers = []
for x in dow_tickers:
    all_major_stocks_tickers.append(x)

for x in nasdaq_tickers:
    all_major_stocks_tickers.append(x)

for x in sp500_tickers:
    all_major_stocks_tickers.append(x)


##Ticker comes from user input in UI, as well as strike
def callVolatility(ticker, strike):
    callChart = options.get_calls(ticker)
    csv = callChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    oneRowDataframe = tickerDf.loc[tickerDf['Strike'] == strike]
    volatility = oneRowDataframe.iloc[0]['Implied Volatility']
    return volatility


def callPercentChange(ticker, strike):
    callChart = options.get_calls(ticker)
    csv = callChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    oneRowDataframe = tickerDf.loc[tickerDf['Strike'] == strike]
    percentChange = oneRowDataframe.iloc[0]['% Change']
    return percentChange

def putVolatility(ticker, strike):
    putChart = options.get_puts(ticker)
    csv = putChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    oneRowDataframe = tickerDf.loc[tickerDf['Strike'] == strike]
    volatility = oneRowDataframe.iloc[0]['Implied Volatility']
    return volatility


def putPercentChange(ticker, strike):
    putChart = options.get_puts(ticker)
    csv = putChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    oneRowDataframe = tickerDf.loc[tickerDf['Strike'] == strike]
    percentChange = oneRowDataframe.iloc[0]['% Change']
    return percentChange

##Optimal day trade for calls is when gamma, delta, volume is highest, theta is lowest
def optimalDayTradeCall(ticker):
    callChart = options.get_calls(ticker)
    csv = callChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    strikeList = tickerDf['Strike'].to_list()
    print(strikeList)

def calculateHedgeRatio(ticker):
    print("hi")

optimalDayTradeCall('nflx')

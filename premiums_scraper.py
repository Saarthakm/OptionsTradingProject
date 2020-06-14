import requests
from yahoo_fin import options
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import yfinance as yf
import bs4
import requests
from bs4 import BeautifulSoup
import mechanize
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.greeks.analytical import gamma
from py_vollib.black_scholes.greeks.analytical import theta
from py_vollib.black_scholes.greeks.analytical import vega
from py_vollib.black_scholes.greeks.analytical import rho
from datetime import date

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

##Optimal day trade for calls is when gamma, delta, volume is highest, theta is lowest, returns optimal STRIKE price
def optimalDayTradeCall(ticker):
    callChart = options.get_calls(ticker)
    csv = callChart.to_csv(ticker + '.csv')
    tickerDf = pd.read_csv(ticker + '.csv')
    strikeList = tickerDf['Strike'].to_list()
    volumeList = tickerDf['Volume'].to_list()
    for i in range(len(volumeList)):
        if volumeList[i] == '-':
            volumeList[i] = int('0')
    #Volume Dictionary has keys as strike prices and values as volume
    volumeDictionary = {}
    keys = strikeList
    x = 0
    for i in keys:
        volumeDictionary[i] = int(volumeList[x])
        x += 1
    sortedLst = sorted([value, key] for (key, value) in volumeDictionary.items())
    rankDictionary = {}

    print(sortedLst)



def calculateHedgeRatio(ticker):
    print("hi")


#optimalDayTradeCall('nflx')

#msft = yf.Ticker("MSFT")
#print(msft.options)
#x = msft.option_chain('2020-06-18')
#dataframeMsft = pd.DataFrame(x)
#print(dataframeMsft)


##add cases for long holds and ER plays
def calculateStopLoss(ticker, strike, optionType):
    if optionType == 'Call' or optionType == 'call':
        callChart = options.get_calls(ticker)
        cdf = pd.DataFrame(callChart)
        oneRowDataframe = cdf.loc[cdf['Strike'] == strike]
        ask = oneRowDataframe.iloc[0]['Ask']
        bid = oneRowDataframe.iloc[0]['Bid']
        currPrice = oneRowDataframe.iloc[0]['Last Price']
        limitPriceUpper = (currPrice - (currPrice * .2)) - (ask - bid)
        limitPriceLower = (currPrice - (currPrice * .15)) - (ask - bid)
        if limitPriceLower < 0 or limitPriceUpper < 0:
            print("No need to set stop loss! This option premium is too low for a stop loss!")
        elif limitPriceUpper != limitPriceLower:
            print("Set Stop Loss Between: $", limitPriceUpper, "and $", limitPriceLower)



    if optionType == 'Put' or optionType == 'Put':
        putChart = options.get_puts(ticker)
        pdf = pd.DataFrame(putChart)
        oneRowDataframe = pdf.loc[pdf['Strike'] == strike]
        ask = oneRowDataframe.iloc[0]['Ask']
        bid = oneRowDataframe.iloc[0]['Bid']
        currPrice = oneRowDataframe.iloc[0]['Last Price']
        limitPriceUpper = (currPrice - (currPrice * .2)) - (ask - bid)
        limitPriceLower = (currPrice - (currPrice * .15)) - (ask - bid)
        if limitPriceLower < 0 or limitPriceUpper < 0:
            print("No need to set stop loss! This option premium is too low for a stop loss!")
        elif limitPriceUpper != limitPriceLower:
            print("Set Stop Loss Between: $", limitPriceUpper, "and $", limitPriceLower)

#helper function, calculates option expiration in years as a decimal (ex: .3845 years)
def optionExpiration(ticker, date):
    today = date.today()
    expireyLst = getOptionExpirationDates(ticker)
    if date in expireyLst:
        x = 1
    else:
        print("This date is not a valid option expiration for this stock!")

def getOptionExpirationDates(ticker):
    expireyLst = options.get_expiration_dates(ticker)
    return expireyLst




print(delta('c', 49, 50, .3846, .05, .2))
print(options.get_expiration_dates('nflx'))

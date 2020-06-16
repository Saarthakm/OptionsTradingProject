import requests
from yahoo_fin import options
import csv
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
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
import datetime
import quandl as q
from yahoo_finance import Share
import matplotlib.pyplot as plt

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
def optimalDayTradeCall(ticker, date):
    callChart = options.get_calls(ticker, date)
    csv = callChart.to_csv(ticker + date + '.csv')
    tickerDf = pd.read_csv(ticker + date + '.csv')
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

#helper function, calculates option expiration in years as a decimal (ex: .3845 years), ASSUMES DATE IS INPUTTED AS XX-XX-XXXX
def optionExpiration(expiration):
    today = datetime.datetime.today()
    todayyr = today.year
    todaymth = today.month
    todayday = today.day
    lst = expiration.split("-")
    expirationyr = int(lst[0])
    expirationmth = int(lst[1])
    expirationday = int(lst[2])
    todayDate = datetime.date(todayyr, todaymth, todayday)
    expirationDate = datetime.date(expirationyr, expirationmth, expirationday)
    delta = expirationDate - todayDate
    return (delta.days / 365)


def getOptionExpirationDates(ticker):
    expireyLst = options.get_expiration_dates(ticker)
    return expireyLst


def calculateGreeks(ticker, date, type, strike):
        S = si.get_live_price(ticker)
        K = strike
        sigma = calculateAnnualizedVolatility(ticker)
        t = optionExpiration(date)
        r = calculateTreasuryYield(date)
        if type == 'Call' or type == "call" or type == "C" or type == 'c':
            flag = 'c'
        else:
            flag = 'p'
        dlta = delta(flag, S, K, t, r, sigma)
        gam = gamma(flag, S, K, t, r, sigma)
        thta = theta(flag, S, K, t, r, sigma)
        vga = vega(flag, S, K, t, r, sigma)
        rh = rho(flag, S, K, t, r, sigma)
        print({"delta": dlta, "gamma": gam, "theta": thta, "vega": vga, "rho": rh})

def calculateTreasuryYield(expirationDate):
    #add case when date is not in table (i.e. gdate is a weekend)
    x = datetime.datetime.today() - datetime.timedelta(days=1)
    y = x.strftime("%Y-%m-%d, %H:%M:%S")
    y = y.split(',')
    y = y[0]
    USYieldTable = q.get("USTREASURY/YIELD")
    csv = USYieldTable.to_csv("treasuryYields.csv")
    ydf = pd.read_csv("treasuryYields.csv")
    ydf = ydf.drop(ydf.columns[[7, 8, 9, 10, 11, 12]], axis=1)
    onerdf = ydf.loc[ydf['Date'] == y]
    timeLst = [1/2, 1/6, 1/4, 1/2, 1, 2]
    timeDict = {"1 MO": 1/2, "2 MO": 1/6, "3 MO": 1/4, "6 MO": 1/2, "1 YR": 1, "2 YR": 2}
    tm = optionExpiration(expirationDate)
    subtractedLst = []
    for i in range(5):
        x = abs(tm - timeLst[i])
        subtractedLst.append(x)
    minIndex = subtractedLst.index(min(subtractedLst))
    finalTime = timeLst[minIndex]
    key_list = list(timeDict.keys())
    val_list = list(timeDict.values())
    final = key_list[val_list.index(finalTime)]
    yieldDecimal = onerdf.iloc[0][final]
    return yieldDecimal


def calculateAnnualizedVolatility(ticker):
    data = yf.download(ticker.upper(), start='2018-6-1', end=date.today())
    data['Log_Ret'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Volatility'] = data['Log_Ret'].rolling(window=252).std() * np.sqrt(252)
    csv = data.to_csv(ticker + 'AnnVol' + '.csv')
    df = pd.read_csv(ticker + 'AnnVol' + '.csv')
    x = datetime.datetime.today() - datetime.timedelta(days=1)
    y = x.strftime("%Y-%m-%d, %H:%M:%S")
    y = y.split(',')
    y = y[0]
    oneRowDataframe = df.loc[df['Date'] == y]
    annualizedVol = oneRowDataframe.iloc[0]['Volatility']
    return float(annualizedVol)



def plotClosingPricesAndAnnualizedVolatility(ticker):
    ata = yf.download(ticker.upper(), start='2018-6-1', end=date.today())
    data['Log_Ret'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Volatility'] = data['Log_Ret'].rolling(window=252).std() * np.sqrt(252)
    data[['Close', 'Volatility']].plot(subplots=True, color='green',figsize=(8, 6))
    plt.show()



#calculateGreeks('ge', '2021-01-15', 'call', 12)
#calculateAnnualizedVolatility('bac')




#converts one type of date to another
#datetime.datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m/%d/%y')

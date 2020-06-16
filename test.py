import numpy as np
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

# Pull NIFTY data from Yahoo finance
NIFTY = yf.download('AAPL',start='2012-6-1', end='2016-6-1')

print(NIFTY)

# Compute the logarithmic returns using the Closing price
#NIFTY['Log_Ret'] = np.log(NIFTY['Close'] / NIFTY['Close'].shift(1))

# Compute Volatility using the pandas rolling standard deviation function
#NIFTY['Volatility'] = NIFTY['Log_Ret'].rolling(window=252).std() * np.sqrt(252)
#print(NIFTY.tail(15))

# Plot the NIFTY Price series and the Volatility
#(NIFTY[['Close', 'Volatility']].plot(subplots=True, color='blue',figsize=(8, 6)))

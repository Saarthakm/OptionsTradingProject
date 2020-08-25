import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from scipy.stats import norm

import Stock as st

amd = st.Stock("COTY")
data = amd.historical_data(3000)
data = data["open"]

log_returns = np.log(1 + data.pct_change())

log_returns.tail()
data.plot(figsize=(10, 6))
u = log_returns.mean()
var = log_returns.var()
drift = u - (0.5 * var)

stdev = log_returns.std()
stdev = np.asarray(stdev)
drift = np.asarray(drift)

x = np.random.rand(10, 2)
x = norm.ppf(x)

Z = norm.ppf(np.random.rand(10, 2))

t_intervals = 1000
iterations = 10

daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(t_intervals, iterations)))
S0 = data.iloc[-1]
price_list = np.zeros_like(daily_returns)
price_list[0] = S0
for t in range(1, t_intervals):
    price_list[t] = price_list[t - 1] * daily_returns[t]

a = np.mean(price_list, axis=1, dtype=np.float64)
print(a)
plt.figure(figsize=(10, 6))
plt.plot(a)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(price_list)
plt.show()
plt.hist(price_list, bins=50)
plt.show()

price_list = np.asarray(price_list)
# pl = []
# for d in range(1, 101):
#     pl.append(np.percentile(price_list,d))
# print(pl)
print("5% quantile =", np.percentile(price_list, 5))
print("95% quantile =", np.percentile(price_list, 95))
# plt.plot(pl)
# plt.show()

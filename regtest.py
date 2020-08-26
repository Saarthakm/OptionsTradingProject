import Stock as st
from Data import data_indicators
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import tulipy as ta
import numpy as np
import pandas as pd
import list
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from statsmodels.formula.api import logit

import seaborn as sns;

sns.set()

# test length when transforming
sc = MinMaxScaler()
b = data_indicators(list.stock_list, 800, "UA", 30)
ticker = "AAPL"
stock = st.Stock(ticker)
df = stock.historical_data(1000)
print("poop")
print(len(df))
df['S_10'] = df['close'].rolling(window=10).mean().fillna(0)
df['Corr'] = df['close'].rolling(window=10).corr(df['S_10']).fillna(0)
# df['RSI'] = ta.RSI(np.array(df['Close']), timeperiod =10)
df['RSI'] = b.compute_rsi(ticker, 10)
df['RSI'] = df['RSI'].fillna(0)
# df = df.fillna('0')
# df.dropna()
df = df.drop(columns=['ticker', 'volume'])
# a = df['open'].to_numpy()
# b = df['close'].to_numpy()
# df['Open-Close'] = np.subtract(a,b)
print(df)
print(len(df))
df['Open-Close'] = df['open'] - df['close'].shift(1)
df['Open-Open'] = df['open'] - df['open'].shift(1)

X = df.iloc[:, :9]
X = X.fillna(0)
print(len(X))

y = np.where(df['close'].shift(-1) > df['close'], 1, -1)
print(y)
split = int(0.7 * len(df))
sc.fit(X)

# X = sc.transform(X)
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

model = LogisticRegression()
# model.max_iter = 10000
model = model.fit(X_train, y_train)
pd.DataFrame((zip(X.columns, np.transpose(model.coef_))), columns=['Variable', 'Coef'])

newdf = X_train
newdf['up_down'] = pd.Series(y_train, index=newdf.index)

newdf['up_down'] = newdf['up_down'].replace(-1, 0)
# We replace all the "-1" by "0", otherwise we'll get the following error message with this library since we need either a 0 or a 1 as dependent variables : "ValueError: endog must be in the unit interval".

model = logit("up_down ~ open + high + low + close + S_10 + Corr + RSI + Open-Close + Open-Open", data=newdf)

results = model.fit()
print(results.summary())
# pd.DataFrame(zip(X.columns, np.transpose(model.coef_)))
# pd.DataFrame((zip(X.columns, np.transpose(model.coef_))), columns = ['Variable', 'Coef'])
# probability = model.predict_proba(X_test)
probability = model.predict_proba(X_test)
# print(probability)
predicted = model.predict(X_test)
df_probability = pd.DataFrame(probability, columns=['0', '1'])
df_predicted = pd.DataFrame(predicted, columns=['Predicted'])
df_probability_predicted = (pd.concat([df_probability, df_predicted],
                                      axis=1, sort=False))
df_probability_predicted['Up/Down'] = np.where(df_probability_predicted['Predicted'] == 1, 'Up', 'Down')
Date = X_test.index
df_probability_predicted.set_index([Date])

a = metrics.confusion_matrix(y_test, predicted)
b = pd.Series(['Actual : -1', 'Actual : 1'])
confusion_matrix = pd.DataFrame(a, columns=['Predicted : -1', 'Predicted : 1'])
confusion_matrix = confusion_matrix.set_index([b])

accuracy = model.score(X_test, y_test)
print(accuracy)
cross_val = cross_val_score(LogisticRegression(), X, y, scoring='accuracy', cv=10)
cross_val
print(cross_val.mean())

df['Predicted_Signal'] = model.predict(X)
df['Original_SP_returns'] = np.log(df['Close'] / df['Close'].shift(1))
Cumulative_originalSP500_returns = np.cumsum(df[split:]['Original_SP_returns'])
df['Strategy_Returns'] = df['Original_SP_returns'] * df['Predicted_Signal'].shift(1)
Cumulative_Strategy_returns = np.cumsum(df[split:]['Strategy_Returns'])

plt.figure(figsize=(10, 20))
plt.plot(Cumulative_originalSP500_returns, color='r', label='aayyymd Returns')
plt.plot(Cumulative_Strategy_returns, color='g', label='Strategy Returns')
plt.legend()
plt.show()

# print(metrics.confusion_matrix(y_test, predicted))
# print(metrics.classification_report(y_test, predicted))
# print(model.score(X_test,y_test))
# cross_val = cross_val_score(LogisticRegression(), X, y, scoring='accuracy', cv=10) #changing cv does some stuff
# print(cross_val)
# print(cross_val.mean())
# df['Predicted_Signal'] = model.predict(X)
# df['returns'] = np.log(df['close']/df['close'].shift(1))
# Cumulative_Nifty_returns = np.cumsum(df[split:]['returns'])
# print(len(df))
# df['Strategy_returns'] = df['returns']* df['Predicted_Signal'].shift(1)
# Cumulative_Strategy_returns = np.cumsum(df[split:]['Strategy_returns'])
# print(len(Cumulative_Strategy_returns))
# print(len(Cumulative_Nifty_returns))
# plt.figure(figsize=(10,20))
# plt.plot(Cumulative_Nifty_returns, color='r',label = 'aayyymd Returns')
# plt.plot(Cumulative_Strategy_returns, color='g', label = 'Strategy Returns')
# plt.legend()
# plt.show()
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
# # regressor = LinearRegression()
# # regressor.fit(X_train, y_train)  # training the algorithm

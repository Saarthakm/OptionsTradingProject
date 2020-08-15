from Data import data_indicators as di
import Stock as st
import list
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import sss as tf
import os
import urllib.request, json
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import BatchNormalization
from keras.optimizers import Optimizer


class lstm_model:
    def aaaaa(self):

        stock = st.Stock("AAPL")
        days = 1000
        dataset = stock.historical_data(days)
        dataset = dataset.dropna()
        dataset_mid = pd.DataFrame()
        dataset_mid["avg"] = dataset[['high', 'low']].mean(axis=1)
        timeframe = len(dataset_mid)
        test_time_frame = int(timeframe * 0.3)
        train_time_frame = timeframe - test_time_frame
        train_data = dataset_mid.head(train_time_frame)

        train_data = train_data.ewm(span=10)['avg'].mean().fillna('-')
        test_data = dataset_mid.tail(test_time_frame).to_numpy()

        # train_data = dataset_mid.head(train_time_frame).to_numpy()

        sc = MinMaxScaler(feature_range=(0, 1))
        sc.fit(train_data)
        training_set_scaled = sc.transform(train_data)

        window = 22
        x_train = []
        y_train = []
        for i in range(window, len(train_data)):
            x_train.append(training_set_scaled[i - window:i, 0])
            y_train.append(training_set_scaled[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        regressor = Sequential()
        regressor.add(LSTM(units=128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        regressor.add(Dropout(.3))
        regressor.add(LSTM(units=128, return_sequences=True))
        regressor.add(Dropout(.3))
        regressor.add(LSTM(units=64, return_sequences=False))
        regressor.add(Dropout(.3))
        regressor.add(Dense(units=1))
        regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['accuracy'])
        history = regressor.fit(x_train, y_train, epochs=380, batch_size=512)
        train_data = train_data.reshape(-1, 1)
        train_data = pd.DataFrame(train_data)
        test_data = pd.DataFrame(test_data)

        dataset_total = pd.concat((train_data[0], test_data[0]), axis=0)

        inputs = dataset_total[len(dataset_total) - len(test_data) - window:].values
        sc.fit(train_data)
        inputs = inputs.reshape(-1, 1)
        inputs = sc.transform(inputs)

        x_test = []
        for i in range(window, len(test_data) + window):  # the range is monkaW
            x_test.append(inputs[i - window:i, 0])
        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predicted_stock_price = regressor.predict(x_test)
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)
        predicted_stock_price = pd.DataFrame(predicted_stock_price)
        predicted_stock_price = predicted_stock_price.iloc[10:]
        real_stock_price = pd.DataFrame(test_data).values
        plt.plot(real_stock_price, color='red', label='EMA of Average Price')
        plt.plot(predicted_stock_price, color='blue', label='Predicted Price Average')
        plt.title('Apple Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Exponential Average of Apple''s price ')
        plt.legend()
        plt.show()


a = lstm_model()
a.aaaaa()

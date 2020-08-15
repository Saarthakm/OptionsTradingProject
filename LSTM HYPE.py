from Data import data_indicators as di
import Stock as st
import list
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


class lstm_model:
    def aaaaa(self):
        window = 220
        stock = st.Stock("AHT")
        timeframe = 5000
        testTime = int(timeframe * .2)
        # testTime = timeframe//10
        dataset = stock.historical_data(timeframe)
        dataset = dataset.dropna()
        dataset_test = pd.DataFrame()
        dataset_test['open'] = dataset['open'].tail(testTime)
        dataset = dataset[:-testTime]
        training_set = dataset['open']
        training_set = pd.DataFrame(training_set)
        sc = MinMaxScaler(feature_range=(0, 1))
        training_set_scaled = sc.fit_transform(training_set)
        x_train = []
        y_train = []
        for i in range(window, len(training_set)):
            x_train.append(training_set_scaled[i - window:i, 0])
            y_train.append(training_set_scaled[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        print(x_train.ndim)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        regressor = Sequential()

        regressor.add(LSTM(units=55, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        regressor.add(Dropout(.41))
        regressor.add(LSTM(units=55, return_sequences=True))
        regressor.add(Dropout(.41))
        regressor.add(LSTM(units=55, return_sequences=True))
        regressor.add(Dropout(.41))
        regressor.add(LSTM(units=55))
        regressor.add(Dropout(.41))
        regressor.add(Dense(units=1))
        regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        model = regressor.fit(x_train, y_train, epochs=150, batch_size=401)
        dataset_total = pd.concat((dataset['open'], dataset_test['open']), axis=0)
        inputs = dataset_total[len(dataset_total) - len(dataset_test) - window:].values

        inputs = inputs.reshape(-1, 1)
        inputs = sc.transform(inputs)

        x_test = []
        for i in range(window, len(dataset_test) + window):  # the range is monkaW
            x_test.append(inputs[i - window:i, 0])
        x_test = np.array(x_test)
        print(x_test.ndim)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        print(x_test.ndim)
        predicted_stock_price = regressor.predict(x_test)
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)
        predicted_stock_price = pd.DataFrame(predicted_stock_price)
        real_stock_price = dataset_test.values
        plt.plot(real_stock_price, color='red', label='Real Apple Stock Price')
        plt.plot(predicted_stock_price, color='blue', label='Predicted Apple Stock Price')
        plt.title('Apple Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Apple Stock Price')
        # plt.plot(model.history['accuracy'], label = 'training loss')
        # plt.plot(model.history['val_acc'], label = 'test loss')
        # plt.xlabel("training loss")
        # plt.ylabel("test loss")
        plt.legend()
        plt.show()


a = lstm_model()
a.aaaaa()

import Stock as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import BatchNormalization


class lstm_model:
    def aaaaa(self):
        # Creates a custom Stock object and gets the data (2000)
        stock = st.Stock("AA")
        days = 200
        dataset = stock.historical_data(days)
        dataset = dataset.dropna()
        dataset_mid = pd.DataFrame()

        # Average price of the day based on high and low
        dataset_mid["avg"] = dataset[['high', 'low']].mean(axis=1)
        timeframe = len(dataset_mid)

        # 30 percent for testing 70 for training
        test_time_frame = int(timeframe * 0.3)
        train_time_frame = timeframe - test_time_frame
        smoothing_time = train_time_frame - test_time_frame
        test_data = dataset_mid.tail(test_time_frame).to_numpy()
        train_data = dataset_mid.head(train_time_frame).to_numpy()
        print(train_data)
        sc = MinMaxScaler(feature_range=(0, 1))
        sc.fit(train_data)
        training_set_scaled = sc.transform(train_data)

        smoothing_window = int(smoothing_time * .25)
        # Smoothes the training data with ema and a smoothing loop
        EMA = 0.0
        gamma = .1
        for ti in range(len(train_data)):
            EMA = gamma * train_data[ti] + (1 - gamma) * EMA
            train_data[ti] = EMA

        for di in range(0, smoothing_time, smoothing_window):
            sc.fit((train_data[di:di + smoothing_window]))
            training_set_scaled[di:di + smoothing_window] = sc.transform((train_data[di:di + smoothing_window]))
            sc.fit((train_data[di + smoothing_window:, :]))
            training_set_scaled[di + smoothing_window:, :] = sc.transform(train_data[di + smoothing_window:, :])

        window = 100
        x_train = []
        y_train = []
        for i in range(window, len(train_data)):
            x_train.append(training_set_scaled[i - window:i, 0])
            y_train.append(training_set_scaled[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        regressor = Sequential()
        regressor.add(LSTM(units=20, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        regressor.add(BatchNormalization(trainable=True))
        regressor.add(Dropout(.6))
        regressor.add(LSTM(units=10))
        regressor.add(BatchNormalization(trainable=True))
        regressor.add(Dropout(.4))
        regressor.add(Dense(units=5))
        regressor.add(BatchNormalization(trainable=True))
        regressor.add(Dropout(.4))
        regressor.add(Dense(units=3))
        regressor.add(BatchNormalization(trainable=True))
        regressor.add(Dropout(.2))
        regressor.add(Dense(units=1))
        # regressor.add(LSTM(units=10, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        # regressor.add(BatchNormalization())
        # regressor.add(LSTM(units=10))
        # regressor.add(BatchNormalization())
        # regressor.add(Dense(units=1))
        # regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['mse'])
        regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['accuracy'])
        history = regressor.fit(x_train, y_train, epochs=50, batch_size=4)
        # history = regressor.fit(x_train, y_train, epochs=150, batch_size=4, validation_split=.30)
        train_data = pd.DataFrame(train_data)
        test_data = pd.DataFrame(test_data)

        dataset_total = pd.concat((train_data[0], test_data[0]), axis=0)

        inputs = dataset_total[len(dataset) - len(test_data) - window:].values
        sc.fit(train_data)
        inputs = inputs.reshape(-1, 1)
        inputs = sc.transform(inputs)

        x_test = []
        for i in range(window, len(test_data) + window):  # the range is monkaW
            x_test.append(inputs[i - window:i, 0])
        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predicted_stock_price = regressor.predict(x_test)
        # print(history.history['loss'])
        # print(history.history['accuracy'])
        # print(history.history['val_loss'])
        # print(history.history['val_accuracy'])
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)
        predicted_stock_price = pd.DataFrame(predicted_stock_price)
        predicted_stock_price = predicted_stock_price.iloc[10:]
        real_stock_price = pd.DataFrame(test_data).values
        plt.plot(real_stock_price, color='red', label='EMA of Average Price')
        plt.plot(predicted_stock_price, color='blue', label='Predicted Price Average')
        plt.title('Apple Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Exponential Average of Apple''s price ')
        # plt.plot(model.history['accuracy'], label = 'training loss')
        # plt.plot(model.history['val_acc'], label = 'test loss')
        # plt.xlabel("training loss")
        # plt.ylabel("test loss")
        plt.legend()
        plt.show()


a = lstm_model()
a.aaaaa()

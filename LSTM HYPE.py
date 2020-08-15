
import Stock as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


class lstm_model:
    def aaaaa(self, hist, epoch, batch_size, window, dropout, unit1, unit2, unit3, unit4):

        stock = st.Stock("AAPL")

        dataset = stock.historical_data(hist)
        dataset = dataset.dropna()
        dataset_mid = pd.DataFrame()
        dataset_mid["avg"] = dataset[['high', 'low']].mean(axis=1)
        timeframe = len(dataset_mid)
        test_time_frame = int(timeframe * .20)
        train_time_frame = timeframe - test_time_frame

        test_data = dataset_mid.tail(test_time_frame).to_numpy()
        train_data = dataset_mid.head(train_time_frame).to_numpy()

        smoothing_time = train_time_frame - test_time_frame

        sc = MinMaxScaler(feature_range=(0, 1))

        sc.fit(train_data)
        training_set_scaled = sc.transform(train_data)

        smoothing_window = int(smoothing_time * .25)

        for di in range(0, smoothing_time, smoothing_window):
            sc.fit((train_data[di:di + smoothing_window]))
            training_set_scaled[di:di + smoothing_window] = sc.transform((train_data[di:di + smoothing_window]))
            sc.fit((train_data[di + smoothing_window:, :]))
            training_set_scaled[di + smoothing_window:, :] = sc.fit_transform(train_data[di + smoothing_window:, :])

        EMA = 0.0
        gamma = .1
        for ti in range(len(train_data)):
            EMA = gamma * train_data[ti] + (1 - gamma) * EMA
            train_data[ti] = EMA

        x_train = []
        y_train = []
        for i in range(window, len(train_data)):
            x_train.append(training_set_scaled[i - window:i, 0])
            y_train.append(training_set_scaled[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        regressor = Sequential()
        regressor.add(LSTM(units=unit1, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        regressor.add(Dropout(dropout))
        regressor.add(LSTM(units=unit2, return_sequences=True))
        regressor.add(Dropout(dropout))
        regressor.add(LSTM(units=unit3, return_sequences=True))
        regressor.add(Dropout(dropout))
        regressor.add(LSTM(units=unit4))
        regressor.add(Dropout(dropout))
        regressor.add(Dense(units=1))
        # regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['mse'])
        regressor.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['accuracy'])
        history = regressor.fit(x_train, y_train, epochs=epoch, batch_size=batch_size, verbose=0)
        # history = regressor.fit(x_train, y_train, epochs=150, batch_size=4, validation_split=.30)
        train_data = pd.DataFrame(train_data)
        test_data = pd.DataFrame(test_data)

        dataset_total = pd.concat((train_data[0], test_data[0]), axis=0)

        inputs = dataset_total[len(dataset_total) - len(test_data) - window:].values
        sc.fit(train_data)
        inputs = inputs.reshape(-1, 1)
        inputs = sc.transform(inputs)

        x_test = []
        for i in range(window, len(test_data) + window + 1):  # the range is monkaW
            x_test.append(inputs[i - window:i, 0])
        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predicted_stock_price = regressor.predict(x_test)
        # print(history.history['loss'])
        # print(history.history['accuracy'])
        # print(history.history['val_loss'])
        # print(history.history['val_accuracy'])
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)
        df = []
        f = 0
        test_data = test_data.to_numpy()
        for i in range(10, len(test_data) - 1):
            p = predicted_stock_price[i] - predicted_stock_price[i + 1]
            r = test_data[i] - test_data[i + 1]
            if (p < 0 and r < 0):
                df.append(True)
            elif (p > 0 and r > 0):
                df.append(True)
            else:
                df.append(False)
                f += 1
        length = len(test_data) - 11
        t = length - f
        return (t / length)

        # predicted_stock_price = pd.DataFrame(predicted_stock_price)
        # predicted_stock_price = predicted_stock_price.iloc[10:]
        # # real_stock_price = pd.DataFrame(test_data).values
        # real_stock_price = pd.DataFrame(test_data)
        #
        # plt.plot(real_stock_price, color='red', label='EMA of Average Price')
        # plt.plot(predicted_stock_price, color='blue', label='Predicted Price Average')
        # plt.title('Apple Stock Price Prediction')
        # plt.xlabel('Time')
        # plt.ylabel('Exponential Average of Apple''s price ')
        # # plt.plot(model.history['accuracy'], label = 'training loss')
        # # plt.plot(model.history['val_acc'], label = 'test loss')
        # # plt.xlabel("training loss")
        # # plt.ylabel("test loss")
        # plt.legend()
        # plt.show()

    def testing_hp(self):
        hist = [1000, 2000, 3000, 4000, 5000]
        epoch = [30, 50, 80, 100, 120, 140, 160, 200]
        batch_size = [4, 8, 16, 32, 64, 128, 256, 512]
        window = [20, 40, 50, 60, 80, 100]
        dropout = [.1, .2, .3, .4]
        unit1 = [4, 6, 8, 10, 15, 20, 30, 40, 50, 75, 100]
        unit2 = [4, 6, 8, 10, 15, 20, 30, 40, 50, 75, 100]
        unit3 = [4, 6, 8, 10, 15, 20, 30, 40, 50, 75, 100]
        unit4 = [4, 6, 8, 10, 15, 20, 30, 40, 50, 75, 100]
        for h in hist:
            for e in epoch:
                for b in batch_size:
                    for w in window:
                        for d in dropout:
                            for u in unit1:
                                for un in unit2:
                                    for uni in unit3:
                                        for unit in unit4:
                                            print("now testing " + " history= " + str(h) + " epoch= " +
                                                  str(e) + " batch= " + str(b) + " window= " + str(w) + " dropout= " +
                                                  str(d) + " layer1 =" + str(u) + " layer2 =" + str(
                                                un) + " layer3 =" + str(uni) +
                                                  " layer4 =" + str(unit))
                                            print("ACCURACY=" + str(self.aaaaa(h, e, b, w, d, u, un, uni, unit)))

a = lstm_model()
a.testing_hp()

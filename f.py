import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import Stock as st
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


# convert an array of values into a dataset matrix

def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + 1:i + look_back + 1, 0])
    x_var = numpy.array(dataX).reshape(-1, look_back)
    y_var = numpy.array(dataY).reshape(-1, look_back)
    return x_var, y_var


# fix random seed for reproducibility
numpy.random.seed(7)
# load the dataset
stock = st.Stock("AAPL")
dataframe = stock.historical_data(5000)
dataset = dataframe["open"].values

dataset = dataset.astype('float32')
# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = dataset.reshape(-1, 1)

dataset = scaler.fit_transform(dataset)
# split into train and test sets
train_size = int(len(dataset) * 0.9)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
# reshape into X=t and Y=t+1
look_back = 4
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))
# create and fit the LSTM network
batch_size = 1
model = Sequential()
# maybe the shape is WONK
model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))
# model.add(LSTM(4, stateful=True))
# model.add(Dropout(.1))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics="accuracy")
for i in range(1):
    model.fit(trainX, trainY, epochs=10, batch_size=batch_size, verbose=1, shuffle=False)
    model.reset_states()
# make predictions
trainPredict = model.predict(trainX, batch_size=batch_size)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)  # ?
# calculate root mean squared error
# trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
# print('Test Score: %.2f RMSE' % (testScore))
# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(dataset) - len(testPredict):] = testPredict
# testPredictPlot[len(trainPredict) + (look_back * 2) +1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
dataset = scaler.inverse_transform(dataset)

plt.plot(dataset)

plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

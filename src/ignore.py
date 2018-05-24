import numpy as np
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.layers import Dense, Input
from keras.layers.recurrent import LSTM
from keras.models import Model

# https://stackoverflow.com/questions/37232782/nan-loss-when-training-regression-network

WINDOW_LENGTH = 5
s = np.arange(0,200).reshape(-1,2)
data = s
target = s / 5
data_gen = TimeseriesGenerator(data, target, length=WINDOW_LENGTH,
                               sampling_rate=1, batch_size=1)
print(len(data_gen))
data_dim = 2
input1 = Input(shape=(WINDOW_LENGTH, data_dim))
lstm1 = LSTM(100, return_sequences=False)(input1)
#lstm2 = LSTM(100)(lstm1)
hidden = Dense(20, activation='relu')(lstm1)
output = Dense(data_dim, activation='linear')(hidden)

model = Model(inputs=input1, outputs=output)
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

model.fit_generator(generator=data_gen,
                    steps_per_epoch=10,
                    epochs=200)
print(model.predict_generator(generator=data_gen, steps=10))


import tensorflow.keras as k
from tensorflow.keras import metrics
import numpy as np
import datetime
from modules.matchups import Matchups
from modules.loss_function import get_loss_single


# maybe also load test data, and predict data!
def get_train_data():
    matchups = Matchups()
    completed_matchups = matchups.get_completed_matchups(until_year=2019)
    split = 10000
    data_x = list(map(lambda completed_matchup: completed_matchup.get_features(), completed_matchups))
    data_y = list(map(lambda completed_matchup: completed_matchup.result, completed_matchups))
    train_x = data_x[:split]
    train_y = data_y[:split]
    test_x  = data_x[split:split+split]
    test_y  = data_y[split:split+split]

    # normalize data
    train_x = np.array(train_x)
    train_y = np.array(train_y)
    test_x = np.array(test_x)
    test_y = np.array(test_y)
    print("finished loading train data")
    return np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y)


def train_model():
    train_x, train_y, test_x, test_y = get_train_data()
    print(len(train_x), len(train_y))
    # Create neural network architecture
    model = k.Sequential()
    model.add(k.layers.Dense(len(train_x), input_dim=len(train_x[0]), activation='sigmoid'))
    model.add(k.layers.Dense(600, activation='sigmoid'))
    model.add(k.layers.Dense(1, activation='sigmoid'))

    # optimizer - sgd, rmsprop
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=[metrics.binary_accuracy])
    model.fit(np.array(train_x), np.array(train_y), validation_split=0.25, epochs=40, batch_size=100)

    test_loss, test_acc = model.evaluate(test_x, test_y)

    print('Test accuracy:', test_acc)
    print('Test loss:', test_loss)

    date_str = str(datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p"))
    model.save('keras_models/{}.h5'.format(date_str))

train_model()

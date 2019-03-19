import tensorflow.keras as k
from tensorflow.keras import metrics
import numpy as np
import datetime
from modules.matchups import Matchups
from modules.loss_function import get_loss_single
import random

# maybe also load test data, and predict data!
def get_train_data(train_num=10000, shuffle=False, until_year= 2015):
    matchups = Matchups()
    completed_matchups = matchups.get_completed_matchups(until_year=until_year)
    train_x = list(map(lambda completed_matchup: completed_matchup.get_features(), completed_matchups))
    train_y = list(map(lambda completed_matchup: completed_matchup.result, completed_matchups))
    if not shuffle:
        train_x = train_x[:train_num]
        train_y = train_y[:train_num]
    else:
        random.seed(1) # set a seed so we could replicate the output
        random_index = random.randint(0, len(train_x)-1, train_num)
        train_x = train_x[random_index]
        train_y = train_y[random_index]
        print(len(train_x), len(train_y))
    # normalize data
    train_x = np.array(train_x)
    train_y = np.array(train_y)
    print("finished loading train data")
    return np.array(train_x), np.array(train_y)


def get_test_data():
    matchups = Matchups()
    completed_matchups_test = matchups.get_completed_matchups(first_year=2016, until_year=2018, post_season_only=True)
    test_x = list(map(lambda completed_matchups_test: completed_matchups_test.get_features(), completed_matchups_test))
    test_y = list(map(lambda completed_matchups_test: completed_matchups_test.result, completed_matchups_test))
    print("finished loading test data")
    return np.array(test_x), np.array(test_y)

def train_model():
    train_x, train_y = get_train_data(until_year=2015, shuffle=True)
    test_x, test_y = get_test_data()
    print(len(train_x), len(train_y))
    # Create neural network architecture
    model = k.Sequential()
    model.add(k.layers.Dense(len(train_x), input_dim=len(train_x[0]), activation='sigmoid'))
    model.add(k.layers.Dense(600, activation='sigmoid'))
    model.add(k.layers.Dense(1, activation='sigmoid'))

    # optimizer - sgd, rmsprop
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=[metrics.binary_accuracy])
    model.fit(np.array(train_x), np.array(train_y), validation_split=0.25, epochs=40, batch_size=100)
    # model.fit(np.array(train_x), np.array(train_y), validation_data=(test_x, test_y), epochs=1, batch_size=1000)

    test_loss, test_acc = model.evaluate(np.array(train_x), np.array(train_y))
    test_loss_test, test_acc_test = model.evaluate(np.array(test_x), np.array(test_y))

    print('Test accuracy:', test_acc)
    print('Test accuracy for march madness 2016-2018:', test_acc_test)

    date_str = str(datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p"))
    model.save('keras_models/{}.h5'.format(date_str))

train_model()

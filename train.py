import tensorflow.keras as k
from tensorflow.keras import metrics
import numpy as np
import datetime
import random
import os

from modules.models.match import Match
from modules.matchups import Matchups
from modules.utilities.file import write_to_file, write_to_json

file_path = os.path.dirname(__file__)
keras_models_directory = os.path.join(file_path, 'keras_models')

params = {
    'EPOCHS': 1,
    'BATCH_SIZE': 100,
    'VALIDATION_SPLIT': .25,
    'OPTIMIZER': 'rmsprop',
    'LOSS_FUNCTION': 'binary_crossentropy',
    'SHUFFLE_TRAINING_DATA': True,
    'INPUT_LAYER': {
        'TYPE': 'Dense',
        'ACTIVATION': 'sigmoid'
    },
    'HIDDEN_LAYERS': [
        {
            'TYPE': 'Dense',
            'NUM_NODES': 600,
            'ACTIVATION': 'sigmoid'
        }
    ],
    'OUTPUT_LAYER': {
        'TYPE': 'Dense',
        'NUM_NODES': 1,
        'ACTIVATION': 'sigmoid'
    }
}


# maybe also load test data, and predict data!
def get_train_data(train_num=10000, shuffle=False, until_year= 2015,  post_season_only=False, regular_season_only=False):
    matchups = Matchups()
    completed_matchups = matchups.get_completed_matchups(until_year=until_year,
                                                         post_season_only=post_season_only,
                                                         regular_season_only=regular_season_only)
    train_x = list(map(lambda completed_matchup: completed_matchup.get_features(), completed_matchups))
    train_y = list(map(lambda completed_matchup: completed_matchup.result, completed_matchups))
    if shuffle:
        random.seed(1)
        random.shuffle(train_x)
        random.shuffle(train_y)
    train_x = train_x[:train_num]
    train_y = train_y[:train_num]
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


def train_model(train_num=10000, shuffle_training=False, regular_season_only=False, post_season_only=False):
    train_x, train_y = get_train_data(train_num=train_num, until_year=2015, shuffle=shuffle_training,
                                      regular_season_only=regular_season_only, post_season_only= post_season_only)
    test_x, test_y = get_test_data()
    print(len(train_x), len(train_y))

    # Create neural network architecture
    model = k.Sequential()

    input_layer = k.layers.Dense(len(train_x), input_dim=len(train_x[0]),
                                                          activation=params['INPUT_LAYER']['ACTIVATION'])
    model.add(input_layer)

    for hidden_layer_data in params['HIDDEN_LAYERS']:
        hidden_layer = k.layers.Dense(hidden_layer_data['NUM_NODES'],
                                                           activation=hidden_layer_data['ACTIVATION'])
        model.add(hidden_layer)

    output_layer = k.layers.Dense(params['OUTPUT_LAYER']['NUM_NODES'],
                                                            activation=params['OUTPUT_LAYER']['ACTIVATION'])
    model.add(output_layer)

    # optimizer - sgd, rmsprop
    model.compile(loss=params['LOSS_FUNCTION'], optimizer=params['OPTIMIZER'], metrics=[metrics.binary_accuracy])
    model.fit(np.array(train_x), np.array(train_y), validation_split=params['VALIDATION_SPLIT'],
              epochs=params['EPOCHS'], batch_size=params['BATCH_SIZE'])

    test_loss_test, test_acc_test = model.evaluate(np.array(test_x), np.array(test_y))

    print('march madness 2016-2018: loss {},   accuracy {},  :'.format(test_loss_test, test_acc_test))

    date_str = str(datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p"))
    os.makedirs(os.path.join(keras_models_directory, date_str))
    model.save('{}/{}/model.h5'.format(keras_models_directory, date_str))
    write_to_json(os.path.join(keras_models_directory, date_str, 'features.json'), Match.get_features_list())
    write_to_json(os.path.join(keras_models_directory, date_str, 'params.json'), params)
    write_to_json(os.path.join(keras_models_directory, date_str, 'accuracy.json'), { 'loss': str(test_loss_test), 'accuracy': str(test_acc_test) })


train_model(train_num=10000, shuffle_training=False, regular_season_only=False, post_season_only=False)

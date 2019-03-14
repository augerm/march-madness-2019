import train

def test_train_data_import():
    train_x, train_y =  train.get_train_data()
    assert(len(train_x) == len(train_y))

# def test_train_mode():
#     train.train_model()

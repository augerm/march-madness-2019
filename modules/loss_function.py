import numpy as np


def get_loss(predicted_results, real_results):
    """
    function to get loss regarding to Kaggle
    :param predicted_results:  list of values?
    :param real_results:  list of values
    :return:  the result of loss = -1/n * sum(yi log (yi_predict) + (1-yi) log (1-yi_predict))
    """
    predicted_results = np.array(predicted_results)
    real_results = np.array(real_results)
    assert(len(predicted_results) == len(real_results))
    num = len(predicted_results)
    loss = -1./num * np.sum(real_results * np.log(predicted_results) + (1-real_results) * np.log(1-predicted_results))
    return loss

def get_loss_single(predicted_results, real_results):
    """
    function to get loss regarding to Kaggle
    :param predicted_results:  list of values?
    :param real_results:  list of values
    :return:  the result of loss = -1/n * sum(yi log (yi_predict) + (1-yi) log (1-yi_predict))
    """
    predicted_results = np.array(predicted_results)
    num = 1
    loss = -1./num * np.sum(real_results * np.log(predicted_results) + (1-real_results) * np.log(1-predicted_results))
    return loss
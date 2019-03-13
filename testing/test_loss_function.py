import modules.loss_function as loss_function
import numpy as np


def test_loss_function_1():
    # A = [1, 1, 1, 1]
    # B = [1, 1, 1, 1]
    # assert(loss_function.get_loss(predicted_results=A, real_results=B) == 0)
    A = [0.1,0.1]
    B = [1,1]
    assert(loss_function.get_loss(A, B) == -np.log(0.1))



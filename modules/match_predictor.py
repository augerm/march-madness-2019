from tensorflow.keras.models import load_model
import numpy as np
class MatchPredictor:
    def __init__(self):
        self.model = load_model('keras_models/19-March-2019-02-49AM.h5')

    def get_result(self, match):
        x = np.array([match.get_features()])
        return self.model.predict(x)[0][0]

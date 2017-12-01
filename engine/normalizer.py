import numpy as np


class Normalizer:
    @staticmethod
    def normalize(vector):
        norm = np.linalg.norm(vector)

        return np.divide(vector, norm)
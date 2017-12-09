import scipy.sparse
import scipy.sparse.linalg


class Normalizer:
    @staticmethod
    def normalize(matrix):
        rows, cold = matrix.shape

        for i in range(rows):
            norm = scipy.sparse.linalg.norm(matrix[i, :])
            matrix[i, :] /= norm

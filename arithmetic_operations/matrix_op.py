import pandas as pd
import numpy as np
from typing import List, Union


class MatrixOperations:

    @classmethod
    def cross_correlation_matrix(cls, matrix1: pd.DataFrame, matrix2: pd.DataFrame):
        pearson_corr = matrix1.corrwith(matrix2, axis=0)
        return pearson_corr

    @classmethod
    def correlation_matrix(cls, matrix: pd.DataFrame):
        return matrix.corr()

    @classmethod
    def flatten_matrix(cls, matrix: np.array):
        return matrix.flatten()

    @classmethod
    def is_symmetric(cls, matrix, rtol=1e-05, atol=1e-08):
        return np.allclose(matrix, matrix.T, rtol=rtol, atol=atol)

    @classmethod
    def drop_symmetric_side_of_a_matrix(cls, matrix: pd.DataFrame, drop_diagonal: bool = True):
        if not cls.is_symmetric(matrix):
            raise (ValueError, "Input matrix shape should be symmetric")
        h, w = matrix.shape
        # Wa want the main diagonal with no off-set
        k = 0
        if drop_diagonal:
            # Set np.nan in diagonal position
            matrix.values[np.diag_indices(h)] = np.nan
        # Pull the lower triangle of the symmetric matrix and flatten the results
        lower_triangle: np.array = matrix.values[np.tril_indices(h, k=k)]
        # Drop nan values if existed
        lower_triangle = lower_triangle[~np.isnan(lower_triangle)]
        return lower_triangle

    @classmethod
    def get_avg_matrix(cls, matrices: List[Union[np.array, pd.DataFrame]], axis: int = 0):
        matrices: List[np.array] = [mat for mat in matrices]
        avg_mat: np.array = np.mean(matrices, axis=axis)
        return avg_mat

    @classmethod
    def get_avg_vector(cls, vec: pd.Series):
        return vec.mean()

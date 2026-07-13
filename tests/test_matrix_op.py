"""arithmetic_operations.matrix_op.MatrixOperations."""
import numpy as np
import pandas as pd
import pytest

from arithmetic_operations.matrix_op import MatrixOperations as M


def test_correlation_matrix():
    df = pd.DataFrame({"a": [1.0, 2, 3, 4], "b": [1.0, 2, 3, 4], "c": [4.0, 3, 2, 1]})
    corr = M.correlation_matrix(df)
    assert np.isclose(corr.loc["a", "b"], 1.0)
    assert np.isclose(corr.loc["a", "c"], -1.0)


def test_cross_correlation_matrix_column_wise():
    m1 = pd.DataFrame({"a": [1.0, 2, 3, 4], "b": [1.0, 2, 3, 4]})
    m2 = pd.DataFrame({"a": [1.0, 2, 3, 4], "b": [4.0, 3, 2, 1]})
    out = M.cross_correlation_matrix(m1, m2)  # correlate matching columns
    assert np.isclose(out["a"], 1.0)
    assert np.isclose(out["b"], -1.0)


def test_flatten_matrix():
    assert list(M.flatten_matrix(np.array([[1, 2], [3, 4]]))) == [1, 2, 3, 4]


def test_is_symmetric():
    assert M.is_symmetric(np.array([[1.0, 2], [2, 1]]))
    assert not M.is_symmetric(np.array([[1.0, 2], [3, 1]]))


def test_drop_symmetric_side_drops_diagonal():
    """drop_diagonal=True returns the strict lower triangle (self-correlations excluded)."""
    m = pd.DataFrame([[1.0, 2, 3], [2, 1, 4], [3, 4, 1]])
    out = M.drop_symmetric_side_of_a_matrix(m, drop_diagonal=True)
    assert sorted(out.tolist()) == [2.0, 3.0, 4.0]


def test_drop_symmetric_side_keeps_diagonal_when_requested():
    m = pd.DataFrame([[1.0, 2, 3], [2, 1, 4], [3, 4, 1]])
    out = M.drop_symmetric_side_of_a_matrix(m, drop_diagonal=False)
    assert sorted(out.tolist()) == [1.0, 1.0, 1.0, 2.0, 3.0, 4.0]


def test_drop_symmetric_side_does_not_mutate_input():
    m = pd.DataFrame([[1.0, 2], [2, 1]])
    M.drop_symmetric_side_of_a_matrix(m, drop_diagonal=True)
    assert m.values[0, 0] == 1.0 and not np.isnan(m.values).any()  # input untouched


def test_drop_symmetric_side_on_asymmetric_raises_valueerror():
    asym = pd.DataFrame([[1.0, 2], [3, 4]])
    with pytest.raises(ValueError):
        M.drop_symmetric_side_of_a_matrix(asym)


def test_get_avg_matrix():
    a = np.array([[1.0, 2], [3, 4]])
    b = np.array([[3.0, 4], [5, 6]])
    assert np.allclose(M.get_avg_matrix([a, b]), [[2.0, 3], [4, 5]])


def test_get_avg_vector():
    assert M.get_avg_vector(pd.Series([1.0, 2, 3, 4])) == 2.5

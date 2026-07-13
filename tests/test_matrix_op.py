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


def test_drop_symmetric_side_returns_lower_triangle_including_diagonal():
    """Pins CURRENT behavior. FLAG: drop_diagonal=True has NO effect — `matrix.values[...] = nan`
    writes to df.values (a copy), so the diagonal is never blanked and appears in the result."""
    m = pd.DataFrame([[1.0, 2, 3], [2, 1, 4], [3, 4, 1]])
    out = M.drop_symmetric_side_of_a_matrix(m.copy(), drop_diagonal=True)
    # lower triangle WITH the (undropped) diagonal: the three 1.0 self-values are still present
    assert sorted(out.tolist()) == [1.0, 1.0, 1.0, 2.0, 3.0, 4.0]


def test_drop_symmetric_side_does_not_actually_mutate_or_drop_diagonal():
    """FLAG: the in-place `matrix.values[diag] = nan` targets a copy, so neither the input is
    mutated nor is the diagonal dropped."""
    m = pd.DataFrame([[1.0, 2], [2, 1]])
    M.drop_symmetric_side_of_a_matrix(m, drop_diagonal=True)
    assert not np.isnan(m.values).any()  # input left unchanged


def test_drop_symmetric_side_on_asymmetric_raises():
    """FLAG: `raise (ValueError, msg)` raises a tuple -> TypeError, not the intended ValueError."""
    asym = pd.DataFrame([[1.0, 2], [3, 4]])
    with pytest.raises(TypeError):
        M.drop_symmetric_side_of_a_matrix(asym)


def test_get_avg_matrix():
    a = np.array([[1.0, 2], [3, 4]])
    b = np.array([[3.0, 4], [5, 6]])
    assert np.allclose(M.get_avg_matrix([a, b]), [[2.0, 3], [4, 5]])


def test_get_avg_vector():
    assert M.get_avg_vector(pd.Series([1.0, 2, 3, 4])) == 2.5

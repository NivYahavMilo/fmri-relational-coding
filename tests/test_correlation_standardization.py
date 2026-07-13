"""arithmetic_operations.correlation_and_standartization — z-score, pearson_correlation, ssmd."""
import numpy as np
import pandas as pd

from arithmetic_operations.correlation_and_standartization import (
    pearson_correlation,
    ssmd,
    z_score,
)


def test_z_score_standardizes_to_mean0_std1():
    arr = np.array([1.0, 2.0, 3.0, 4.0])
    out = z_score(arr, axis=0)
    assert np.allclose(out, (arr - arr.mean()) / arr.std())  # population std (ddof=0)
    assert np.isclose(out.mean(), 0.0)
    assert np.isclose(out.std(), 1.0)


def test_pearson_correlation_is_xtx_over_n_minus_1():
    """Pins current behavior: (1/(n-1)) * seqᵀ·seq — a covariance-like matrix.

    NOTE: this only equals a true correlation matrix when the columns are already z-scored, and
    even then the diagonal is n/(n-1) rather than exactly 1 (uses ddof=1 while z_score uses ddof=0).
    """
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]})
    out = pearson_correlation(df)
    expected = (1 / (len(df) - 1)) * (df.values.T @ df.values)
    assert np.allclose(out.values, expected)


def test_ssmd_is_standardized_mean_difference():
    """Sum over i of (x_mean - y_mean) / sqrt(x_std**2 + y_std**2)."""
    result = ssmd(x_mean=[3.0, 5.0], x_std=[3.0, 4.0], y_mean=[1.0, 2.0], y_std=[4.0, 3.0])
    expected = (3.0 - 1.0) / np.sqrt(3.0 ** 2 + 4.0 ** 2) + (5.0 - 2.0) / np.sqrt(4.0 ** 2 + 3.0 ** 2)
    assert np.isclose(result, expected)  # == 0.4 + 0.6 == 1.0

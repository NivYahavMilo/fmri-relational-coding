"""arithmetic_operations.decomposition.Decomposition — PCA dimensionality reduction."""
import numpy as np
import pandas as pd

from arithmetic_operations.decomposition import Decomposition


def _data(seed=0, rows=10, cols=4):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(rng.standard_normal((rows, cols)), columns=[f"c{i}" for i in range(cols)])


def test_reduce_dimensions_int_components_shape_and_columns():
    data = _data(cols=4)
    out = Decomposition.reduce_dimensions(data, n_components=2)
    # data.T (4x10) -> PCA to 2 comps -> transform (4x2) -> transpose -> (2x4); columns preserved
    assert out.shape == (2, 4)
    assert list(out.columns) == list(data.columns)


def test_reduce_dimensions_float_fraction_of_columns():
    data = _data(cols=4)
    # float n_components is interpreted as a fraction of data.shape[1]: 0.5 * 4 -> 2
    out = Decomposition.reduce_dimensions(data, n_components=0.5)
    assert out.shape == (2, 4)


def test_reduce_dimensions_full_rank_is_information_preserving():
    data = _data(rows=8, cols=4)
    # full component count keeps all variance (up to PCA rotation)
    out = Decomposition.reduce_dimensions(data, n_components=4)
    assert out.shape == (4, 4)

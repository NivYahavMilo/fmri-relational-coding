"""arithmetic_operations.distances_utils — pairwise distances between per-movie voxel averages."""
import numpy as np
import pandas as pd

from arithmetic_operations.distances_utils import (
    _calculate_distance_vectors,
    create_distances_movies_vector,
)


def test_calculate_distance_vectors_is_pairwise_abs_mean_distance():
    # columns = movies; per-column mean: m1=0, m2=3, m3=10
    df = pd.DataFrame({"m1": [0.0, 0.0], "m2": [2.0, 4.0], "m3": [10.0, 10.0]})
    out = _calculate_distance_vectors(df)
    expected = pd.DataFrame(
        [[0.0, 3.0, 10.0], [3.0, 0.0, 7.0], [10.0, 7.0, 0.0]], columns=["m1", "m2", "m3"]
    )
    pd.testing.assert_frame_equal(out.reset_index(drop=True), expected, check_dtype=False)


def test_create_distances_movies_vector_splits_clips_and_rests():
    # first half of columns = clips, second half = rests
    df = pd.DataFrame({
        "c1": [0.0, 0.0], "c2": [4.0, 4.0],   # clip means: 0, 4
        "r1": [1.0, 1.0], "r2": [1.0, 1.0],   # rest means: 1, 1
    })
    out = create_distances_movies_vector(df)
    # clip distance matrix (|0-0|,|0-4| / |4-0|,|4-4|) then rest matrix (all zeros) side by side
    assert list(out.columns) == ["c1", "c2", "r1", "r2"]
    np.testing.assert_allclose(out[["c1", "c2"]].to_numpy(), [[0, 4], [4, 0]])
    np.testing.assert_allclose(out[["r1", "r2"]].to_numpy(), [[0, 0], [0, 0]])

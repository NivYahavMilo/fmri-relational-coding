"""rc_core: custom-temporal window extractors."""
import numpy as np
import pytest

import rc_core


def test_task_window_end_averages_last_trs(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=10, n_voxels=2, value_fn=lambda c, t, v: t)
    # init_window='end', size 3 -> timepoints [7,8,9] -> mean 8
    vec = rc_core.get_task_window_slides_vectors(data, clip_i=1, init_window="end", window_size_task=3)
    np.testing.assert_allclose(vec, [8.0, 8.0])


def test_task_window_start_averages_first_trs(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=10, n_voxels=2, value_fn=lambda c, t, v: t)
    # init_window='start', size 3 -> range(0,3) [0,1,2] -> mean 1
    vec = rc_core.get_task_window_slides_vectors(data, clip_i=1, init_window="start", window_size_task=3)
    np.testing.assert_allclose(vec, [1.0, 1.0])


def test_task_window_invalid_init_window_raises(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=5, n_voxels=2, value_fn=lambda c, t, v: t)
    with pytest.raises(ValueError):
        rc_core.get_task_window_slides_vectors(data, clip_i=1, init_window="bogus", window_size_task=3)


def test_rest_window_simple_average(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=19, n_voxels=2, value_fn=lambda c, t, v: t)
    # window (0,5) fully inside available timepoints -> mean of [0..4] = 2
    vec = rc_core.get_rest_window_slides_vectors(data, clip_i=1, window_size_rest=(0, 5))
    np.testing.assert_allclose(vec, [2.0, 2.0])


def test_custom_temporal_relational_coding_returns_bounded_distance(static_data, make_voxel_data):
    # non-collinear per-clip voxel patterns (sin/cos) so the correlations are well-defined
    task = make_voxel_data(clips=range(1, 15), timepoints=12, n_voxels=5,
                           value_fn=lambda c, t, v: np.sin(1.7 * c + 2.3 * v) + 0.05 * t)
    rest = make_voxel_data(clips=range(1, 15), timepoints=19, n_voxels=5,
                           value_fn=lambda c, t, v: np.cos(1.1 * c + 1.9 * v) + 0.03 * t)
    distance, feature_df = rc_core.custom_temporal_relational_coding(
        data_task=task, data_rest=rest, window_size_rest=(0, 5), init_window_task="end", window_size_task=3
    )
    assert isinstance(distance, float)
    assert -1.0 <= distance <= 1.0
    assert feature_df.shape[1] == 28  # 14 task + 14 rest window vectors

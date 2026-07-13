"""relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils — window extractors."""
import numpy as np
import pytest

from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import (
    CustomTemporalRelationalCodingUtils as CT,
)


def test_task_window_end_averages_last_trs(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=10, n_voxels=2, value_fn=lambda c, t, v: t)
    # init_window='end', size 3 -> timepoints [7,8,9] -> mean 8
    vec = CT.get_task_window_slides_vectors(data, clip_i=1, init_window="end", window_size_task=3)
    np.testing.assert_allclose(vec, [8.0, 8.0])


def test_task_window_start_averages_first_trs(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=10, n_voxels=2, value_fn=lambda c, t, v: t)
    # init_window='start', size 3 -> range(0,3) [0,1,2] -> mean 1
    vec = CT.get_task_window_slides_vectors(data, clip_i=1, init_window="start", window_size_task=3)
    np.testing.assert_allclose(vec, [1.0, 1.0])


def test_task_window_invalid_init_window_raises(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=5, n_voxels=2, value_fn=lambda c, t, v: t)
    with pytest.raises(ValueError):
        CT.get_task_window_slides_vectors(data, clip_i=1, init_window="bogus", window_size_task=3)


def test_rest_window_simple_average(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=19, n_voxels=2, value_fn=lambda c, t, v: t)
    # window (0,5) fully inside available timepoints -> mean of [0..4] = 2
    vec = CT().get_rest_window_slides_vectors(data, clip_i=1, window_size_rest=(0, 5))
    np.testing.assert_allclose(vec, [2.0, 2.0])

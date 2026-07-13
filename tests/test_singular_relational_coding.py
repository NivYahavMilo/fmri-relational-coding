"""relational_coding.singular_relational_coding.SingularRelationalCoding."""
import numpy as np

from relational_coding.singular_relational_coding import SingularRelationalCoding


def test_get_avg_rest_matrix_is_mean_over_timepoints(make_voxel_data):
    # clip 1 over 3 timepoints; value = t (same across voxels) -> per-voxel mean of [0,1,2] = 1.0
    data = make_voxel_data(clips=[1, 2], timepoints=3, n_voxels=2, value_fn=lambda c, t, v: t)
    avg = SingularRelationalCoding._get_avg_rest_matrix(data, clip_index=1)
    assert list(avg) == [1.0, 1.0]


def test_singular_relational_coding_matches_task_to_rest_average(static_data, make_voxel_data):
    # task last-TR vector == rest average vector per clip (both = clip*10 + voxel) -> corr = 1.0
    task = make_voxel_data(clips=range(1, 15), timepoints=2, n_voxels=4, value_fn=lambda c, t, v: c * 10 + v)
    rest = make_voxel_data(clips=range(1, 15), timepoints=3, n_voxels=4, value_fn=lambda c, t, v: c * 10 + v)

    out = SingularRelationalCoding().singular_relational_coding(d_task=task, d_rest=rest)

    assert len(out) == 14
    assert set(out.keys()) == {f"clip{i}" for i in range(1, 15)}
    for score in out.values():
        assert np.isclose(score, 1.0)

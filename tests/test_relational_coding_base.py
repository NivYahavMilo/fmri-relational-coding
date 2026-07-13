"""relational_coding.relational_coding_base.RelationalCodingBase — pure helpers + core correlate."""
import numpy as np
import pandas as pd
import pytest

from relational_coding.relational_coding_base import RelationalCodingBase


def test_get_clip_name_by_index(static_data):
    assert RelationalCodingBase.get_clip_name_by_index(1) == "clip1"
    assert RelationalCodingBase.get_clip_name_by_index(14) == "clip14"


def test_rest_between_tr_generator():
    assert list(RelationalCodingBase.rest_between_tr_generator()) == list(range(19))


def test_yield_subject_generator(static_data):
    assert list(RelationalCodingBase.yield_subject_generator()) == ["s1", "s2"]


def test_check_roi_validity(static_data):
    RelationalCodingBase._check_roi_validity("RH_Vis_1")  # valid -> no raise
    with pytest.raises(ValueError):
        RelationalCodingBase._check_roi_validity("NOT_A_ROI")


def test_rearrange_clip_order(static_data):
    cols = static_data.CLIPS_ORDER + static_data.REST_ORDER
    df = pd.DataFrame({c: [float(i)] for i, c in enumerate(reversed(cols))})  # scrambled
    out = RelationalCodingBase.rearrange_clip_order(df)
    assert list(out.columns) == cols


def test_shuffle_rest_vectors_keeps_clips_permutes_rest(static_data):
    cols = static_data.CLIPS_ORDER + static_data.REST_ORDER
    df = pd.DataFrame({c: [1.0] for c in cols})
    np.random.seed(0)
    out = RelationalCodingBase.shuffle_rest_vectors(df)
    assert list(out.columns)[:14] == static_data.CLIPS_ORDER            # clips untouched, in order
    assert sorted(list(out.columns)[14:]) == sorted(static_data.REST_ORDER)  # rests permuted


def test_get_single_tr_vector_defaults_to_last_timepoint(make_voxel_data):
    data = make_voxel_data(clips=[1], timepoints=3, n_voxels=3, value_fn=lambda c, t, v: t * 10 + v)
    # default timepoint=-1 -> last (t=2) -> [20, 21, 22]
    assert RelationalCodingBase.get_single_tr_vector(data, clip_i=1) == [20.0, 21.0, 22.0]


def test_get_single_tr_vector_specific_timepoint(make_voxel_data):
    data = make_voxel_data(clips=[1, 2], timepoints=5, n_voxels=2, value_fn=lambda c, t, v: c * 100 + t * 10 + v)
    # clip 2, timepoint 1 -> 2*100 + 1*10 + v -> [210, 211]
    assert RelationalCodingBase.get_single_tr_vector(data, clip_i=2, timepoint=1) == [210.0, 211.0]


def test_correlate_current_timepoint_identical_task_rest_structure_gives_one(static_data):
    """When each clip's rest vector equals its task vector, the task and rest correlation
    structures are identical, so their correlation (the returned distance) is 1.0."""
    rng = np.random.default_rng(1)
    base = {i: rng.standard_normal(6) for i in range(1, 15)}
    data = {}
    for i in range(1, 15):
        data[f"clip{i}_task"] = base[i].tolist()
        data[f"clip{i}_rest"] = base[i].tolist()

    distance, corr_df = RelationalCodingBase().correlate_current_timepoint(data)
    assert np.isclose(distance, 1.0)
    assert corr_df.shape == (28, 28)


def test_correlate_current_timepoint_returns_bounded_distance(static_data):
    rng = np.random.default_rng(0)
    data = {name: rng.standard_normal(6).tolist()
            for name in static_data.CLIPS_ORDER + static_data.REST_ORDER}
    distance, corr_df = RelationalCodingBase().correlate_current_timepoint(data)
    assert isinstance(distance, float)
    assert -1.0 <= distance <= 1.0
    assert corr_df.shape == (28, 28)

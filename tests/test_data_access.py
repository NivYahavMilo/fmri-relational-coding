"""data_access loaders: ROI validation and pickle-path construction (I/O is stubbed)."""
import os

import pytest

import data_access
import settings
from enums import Mode


@pytest.fixture
def capture_read_pickle(monkeypatch):
    """Replace pd.read_pickle with a recorder; returns a dict holding the requested path."""
    calls = {}

    def fake_read_pickle(path):
        calls["path"] = path
        return "SENTINEL_DF"

    monkeypatch.setattr(data_access.pd, "read_pickle", fake_read_pickle)
    return calls


def test_check_roi_validity(static_data):
    data_access.check_roi_validity("RH_Vis_1")  # known ROI -> no raise
    with pytest.raises(ValueError):
        data_access.check_roi_validity("NOT_AN_ROI")


def test_load_roi_data_path_and_validation(static_data, capture_read_pickle):
    out = data_access.load_roi_data("RH_Vis_1", "s1", Mode.CLIPS)
    assert out == "SENTINEL_DF"
    expected = os.path.join(settings.SUBNET_DATA_DF.format(mode=Mode.CLIPS.value), "s1", "RH_Vis_1.pkl")
    assert capture_read_pickle["path"] == expected


def test_load_roi_data_rejects_unknown_roi(static_data, capture_read_pickle):
    with pytest.raises(ValueError):
        data_access.load_roi_data("BOGUS", "s1", Mode.REST)
    assert "path" not in capture_read_pickle  # failed before any read


def test_load_avg_data_path_uses_group(static_data, capture_read_pickle):
    data_access.load_avg_data("RH_Vis_2", Mode.REST, group="_GROUP1")
    expected = os.path.join(settings.SUBNET_DATA_AVG.format(mode=Mode.REST.value, group="_GROUP1"), "RH_Vis_2.pkl")
    assert capture_read_pickle["path"] == expected


def test_load_group_subjects_path(static_data, capture_read_pickle):
    # note: load_group_subjects intentionally does not validate the ROI name
    data_access.load_group_subjects("RH_Vis_1", Mode.CLIPS, n_subjects=10, group_index=3)
    expected = os.path.join(
        settings.SUBNET_AVG_N_SUBJECTS.format(mode=Mode.CLIPS.value, n_subjects=10, group_i=3), "RH_Vis_1.pkl")
    assert capture_read_pickle["path"] == expected

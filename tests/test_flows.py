"""flows/*.run() orchestration: caching short-circuit, avg/subject routing, and what gets persisted.

The heavy dependencies (disk I/O, the rc_core algorithms) are stubbed; these tests only pin the
glue each flow module is responsible for.
"""
import os

import pytest

import rc_core
import data_access
from data_normalizer import utils
from enums import Mode

import flows.singular as singular
import flows.fmri_relational_coding as frc
import flows.custom_temporal as custom_temporal
import flows.isfc as isfc
import flows.snr as snr
import flows.concat as concat


@pytest.fixture
def saved(monkeypatch):
    """Record calls to utils.dict_to_pkl as (data, path) tuples."""
    calls = []
    monkeypatch.setattr(utils, "dict_to_pkl", lambda data, path: calls.append((data, path)))
    return calls


@pytest.fixture
def no_disk(monkeypatch):
    """Neutralize directory creation so nothing touches the filesystem."""
    monkeypatch.setattr(os, "makedirs", lambda *a, **k: None)
    monkeypatch.setattr(os, "mkdir", lambda *a, **k: None)
    monkeypatch.setattr(os.path, "exists", lambda p: True)


# --------------------------- singular ---------------------------

def test_singular_caches_when_result_exists(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    singular.run("RH_Vis_1")
    assert saved == []  # short-circuited, nothing written


def test_singular_writes_per_subject(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_roi_data", lambda **k: "df")
    monkeypatch.setattr(rc_core, "singular_relational_coding", lambda d_task, d_rest: "RC")
    singular.run("RH_Vis_1")
    assert len(saved) == 1
    data, path = saved[0]
    assert data == {"s1": "RC", "s2": "RC"}
    assert path.endswith("RH_Vis_1") and not path.endswith(".pkl")


# --------------------- fmri_relational_coding -------------------

def test_frc_subject_flow_keys_by_subject(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_roi_data", lambda **k: "df")
    monkeypatch.setattr(frc, "_relation_distance", lambda d_rest, d_task, shuffle: (["dist"], ["corr"]))
    frc.run("RH_Vis_1", avg_data=False)
    data, _ = saved[0]
    assert set(data) == {"s1", "s2"}
    assert data["s1"] == ["dist"]


def test_frc_avg_flow_stores_avg_and_correlation(static_data, saved, monkeypatch):
    monkeypatch.setattr(data_access, "load_avg_data", lambda **k: "df")
    monkeypatch.setattr(frc, "_relation_distance", lambda d_rest, d_task, shuffle: (["dist"], ["corr"]))
    frc.run("RH_Vis_1", avg_data=True, group="_GROUP1")
    data, _ = saved[0]
    assert data["avg"] == ["dist"]
    assert data["avg correlation"] == ["corr"]


def test_frc_shuffle_caches(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    frc.run("RH_Vis_1", avg_data=False, shuffle=True)
    assert saved == []


# ------------------------ custom_temporal ----------------------

def _ct_kwargs(**extra):
    base = dict(rest_window_size=(0, 5), init_window_task="end", task_window_size=10)
    base.update(extra)
    return base


def test_custom_temporal_caches(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    custom_temporal.run("RH_Vis_1", **_ct_kwargs())
    assert saved == []


def test_custom_temporal_subject_flow(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_roi_data", lambda **k: "df")
    monkeypatch.setattr(rc_core, "custom_temporal_relational_coding", lambda **k: (0.5, "vecs"))
    custom_temporal.run("RH_Vis_1", **_ct_kwargs())
    data, _ = saved[0]
    assert set(data) == {"s1", "s2"} and data["s1"] == 0.5


def test_custom_temporal_avg_flow(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_avg_data", lambda **k: "df")
    monkeypatch.setattr(rc_core, "custom_temporal_relational_coding", lambda **k: (0.5, "vecs"))
    custom_temporal.run("RH_Vis_1", average_data=True, **_ct_kwargs())
    data, _ = saved[0]
    assert data == {"avg": 0.5}


# ---------------------------- isfc -----------------------------

def test_isfc_caches(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    isfc.run("RH_Vis_1")
    assert saved == []


def test_isfc_writes_per_subject(static_data, saved, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_roi_data", lambda **k: "task")
    monkeypatch.setattr(isfc, "_load_subjects_average_leave_one_out", lambda roi_name, subject: "rest")
    monkeypatch.setattr(isfc, "_isfc_relational_coding", lambda **k: [1, 2])
    isfc.run("RH_Vis_1")
    data, _ = saved[0]
    assert data == {"s1": [1, 2], "s2": [1, 2]}


# ----------------------------- snr -----------------------------

def test_snr_stores_distance(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(data_access, "load_group_subjects", lambda **k: "df")
    monkeypatch.setattr(rc_core, "custom_temporal_relational_coding", lambda **k: (0.7, "vecs"))
    snr.run("RH_Vis_1", init_window="end", task_ws=10, rest_ws=(0, 5),
            group_subjects=10, group_index=1)
    data, _ = saved[0]
    assert data == {"relational_coding_distance": 0.7}


# ---------------------------- concat ---------------------------

def test_concat_caches(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    concat.run("RH_Vis_1", init_window="end", task_ws=10, rest_ws=(0, 5),
               group_subjects=10, group_index=1)
    assert saved == []


def test_concat_activation_pattern(static_data, saved, no_disk, monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(data_access, "load_group_subjects", lambda **k: "df")
    monkeypatch.setattr(rc_core, "custom_temporal_relational_coding", lambda **k: (None, "tr_df"))
    monkeypatch.setattr(rc_core, "correlate_concatenated_signals", lambda df, **k: (0.9, "signals"))
    concat.run("RH_Vis_1", init_window="end", task_ws=10, rest_ws=(0, 5),
               group_subjects=10, group_index=1)
    data, _ = saved[0]
    assert data == {"activation_pattern": 0.9, "concat_signals": "signals"}

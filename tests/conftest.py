"""Shared test setup for the relational-coding algorithm tests.

Tests exercise the pure arithmetic / algorithmic functions on small synthetic inputs. Some of the
production code calls ``matplotlib.pyplot.show()``, so we force a non-interactive backend to keep
the test run headless.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib

matplotlib.use("Agg")  # no interactive windows during tests

import pandas as pd
import pytest

N_CLIPS = 14


@pytest.fixture
def static_data():
    """Populate StaticData with small, controlled values (mirrors the real JSON structure)."""
    from data_center.static_data.static_data import StaticData

    StaticData.CLIP_MAPPING = {str(i): f"clip{i}" for i in range(1, N_CLIPS + 1)}
    StaticData.CLIPS_ORDER = [f"clip{i}_task" for i in range(1, N_CLIPS + 1)]
    StaticData.REST_ORDER = [f"clip{i}_rest" for i in range(1, N_CLIPS + 1)]
    StaticData.ROI_NAMES = ["RH_Vis_1", "RH_Vis_2"]
    StaticData.SUBJECTS = ["s1", "s2"]
    return StaticData


@pytest.fixture
def make_voxel_data():
    """Build a per-subject voxel table: rows are (clip y, timepoint), columns are voxels + metadata."""
    def _build(clips, timepoints, n_voxels, value_fn, subject="s1"):
        rows = []
        for c in clips:
            for t in range(timepoints):
                row = {v: float(value_fn(c, t, v)) for v in range(n_voxels)}
                row.update({"y": c, "timepoint": t, "Subject": subject})
                rows.append(row)
        return pd.DataFrame(rows)

    return _build

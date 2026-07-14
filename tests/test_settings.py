"""settings.py path roots: study defaults + environment overrides, with derived paths following."""
import importlib
import os

import pytest

import settings as settings_module

ENV_VARS = ["RC_DRIVE", "RC_DATA_DIR", "RC_RESULTS_DIR"]


@pytest.fixture
def reload_settings():
    """Reload settings under the current environment; restore defaults afterwards."""
    def _reload():
        return importlib.reload(settings_module)

    yield _reload
    for key in ENV_VARS:
        os.environ.pop(key, None)
    importlib.reload(settings_module)


def test_defaults(reload_settings, monkeypatch):
    for key in ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    s = reload_settings()
    assert s.MY_BOOK_PATH == os.path.join("/Volumes", "My_Book")
    assert s.DATA_DRIVE_E == os.path.join(s.MY_BOOK_PATH, "parcelled_data_niv")
    assert s.RESULTS_DIR == os.path.join(s.MY_BOOK_PATH, "fmri-relational-coding-results")


def test_env_overrides(reload_settings, monkeypatch):
    monkeypatch.setenv("RC_DRIVE", "/tmp/drive")
    monkeypatch.setenv("RC_DATA_DIR", "/tmp/data")
    monkeypatch.setenv("RC_RESULTS_DIR", "/tmp/results")
    s = reload_settings()
    assert s.MY_BOOK_PATH == "/tmp/drive"
    assert s.DATA_DRIVE_E == "/tmp/data"
    assert s.RESULTS_DIR == "/tmp/results"
    # derived data/results paths follow the overridden roots
    assert s.SUBNET_DATA_DF.format(mode="TASK").startswith("/tmp/data")
    assert s.RELATIONAL_CODING.startswith("/tmp/results")


def test_data_dir_falls_back_to_drive(reload_settings, monkeypatch):
    # only the drive root is overridden; DATA_DRIVE_E should be derived from it
    for key in ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("RC_DRIVE", "/mnt/x")
    s = reload_settings()
    assert s.DATA_DRIVE_E == os.path.join("/mnt/x", "parcelled_data_niv")

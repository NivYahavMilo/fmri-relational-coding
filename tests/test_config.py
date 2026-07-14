"""config.py path roots: study defaults + environment overrides, with derived paths following."""
import importlib
import os

import pytest

import config as config_module

ENV_VARS = ["RC_DRIVE", "RC_DATA_DIR", "RC_RESULTS_DIR"]


@pytest.fixture
def reload_config():
    """Reload config under the current environment; restore defaults afterwards."""
    def _reload():
        return importlib.reload(config_module)

    yield _reload
    for key in ENV_VARS:
        os.environ.pop(key, None)
    importlib.reload(config_module)


def test_defaults(reload_config, monkeypatch):
    for key in ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    c = reload_config()
    assert c.MY_BOOK_PATH == os.path.join("/Volumes", "My_Book")
    assert c.DATA_DRIVE_E == os.path.join(c.MY_BOOK_PATH, "parcelled_data_niv")
    assert c.RESULTS_DIR == os.path.join(c.MY_BOOK_PATH, "fmri-relational-coding-results")


def test_env_overrides(reload_config, monkeypatch):
    monkeypatch.setenv("RC_DRIVE", "/tmp/drive")
    monkeypatch.setenv("RC_DATA_DIR", "/tmp/data")
    monkeypatch.setenv("RC_RESULTS_DIR", "/tmp/results")
    c = reload_config()
    assert c.MY_BOOK_PATH == "/tmp/drive"
    assert c.DATA_DRIVE_E == "/tmp/data"
    assert c.RESULTS_DIR == "/tmp/results"
    # derived data/results paths follow the overridden roots
    assert c.SUBNET_DATA_DF.format(mode="TASK").startswith("/tmp/data")
    assert c.RELATIONAL_CODING.startswith("/tmp/results")


def test_data_dir_falls_back_to_drive(reload_config, monkeypatch):
    # only the drive root is overridden; DATA_DRIVE_E should be derived from it
    for key in ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("RC_DRIVE", "/mnt/x")
    c = reload_config()
    assert c.DATA_DRIVE_E == os.path.join("/mnt/x", "parcelled_data_niv")

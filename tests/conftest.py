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

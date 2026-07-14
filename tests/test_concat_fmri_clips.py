"""rc_core: concatenated-signal correlation."""
import numpy as np
import pandas as pd

import rc_core


def test_correlate_concatenated_signals_returns_bounded_distance():
    rng = np.random.default_rng(0)
    df = pd.DataFrame(rng.standard_normal((5, 28)))
    distance, out = rc_core.correlate_concatenated_signals(df)
    assert isinstance(distance, float)
    assert -1.0 <= distance <= 1.0
    assert list(out.columns) == ["concat_clip", "concat_rest"]


def test_correlate_concatenated_signals_identical_clip_rest_gives_one():
    # even (clip) and odd (rest) columns identical -> concatenated signals identical -> corr 1
    rng = np.random.default_rng(1)
    base = rng.standard_normal((5, 14))
    cols = np.empty((5, 28))
    cols[:, 0::2] = base
    cols[:, 1::2] = base
    distance, _ = rc_core.correlate_concatenated_signals(pd.DataFrame(cols))
    assert np.isclose(distance, 1.0)

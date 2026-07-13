"""arithmetic_operations.signal_processing.SignalProcessing."""
import numpy as np
import pandas as pd

from arithmetic_operations.signal_processing import SignalProcessing


def test_low_pass_filtering_shape_and_attenuates_high_freq():
    t = np.arange(60)
    low = np.sin(2 * np.pi * 0.02 * t)          # slow component (kept)
    high = 0.8 * np.sin(2 * np.pi * 0.4 * t)    # fast component (should be removed)
    sig = low + high
    data = pd.DataFrame({"c0": sig, "c1": sig})

    out = SignalProcessing.low_pass_filtering(data, filter_order=4, cut_off=0.09)

    assert out.shape == (60, 2)
    assert list(out.columns) == ["c0", "c1"]
    # after low-pass the signal is closer to its low-frequency part than the raw input was
    assert np.std(out["c0"].to_numpy() - low) < np.std(sig - low)


def test_get_max_frequency_returns_nonnegative_float_smoke():
    """Smoke test only. FLAG: this indexes the (flattened) data by argmax of the PSD, which is
    dimensionally inconsistent and looks like a bug — see the review notes."""
    data = pd.DataFrame(np.random.default_rng(0).standard_normal((5, 30)))
    val = SignalProcessing._get_max_frequency(data)
    assert isinstance(val, float)
    assert val >= 0.0

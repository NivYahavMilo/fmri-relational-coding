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


def test_get_max_frequency_finds_dominant_frequency():
    t = np.arange(60)
    # three signals, each a 0.1 Hz sinusoid over time (welch runs along axis=1)
    data = pd.DataFrame(np.vstack([np.sin(2 * np.pi * 0.1 * t) for _ in range(3)]))
    val = SignalProcessing._get_max_frequency(data)
    assert 0.0 <= val <= 0.5          # a valid frequency (<= Nyquist)
    assert 0.05 <= val <= 0.2         # near the true 0.1 Hz (within Welch's bin resolution)

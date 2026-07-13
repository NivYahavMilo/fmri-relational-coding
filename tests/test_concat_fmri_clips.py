"""relational_coding.custom_temporal_relational_coding.concat_fmri_clips."""
import numpy as np
import pandas as pd
import pytest

from relational_coding.custom_temporal_relational_coding.concat_fmri_clips import (
    ConcatFmriTemporalRelationalCoding,
)


def test_correlate_concatenated_signals_is_broken_by_zscore_axis_bug():
    """FLAG: `_correlate_concatenated_signals` calls `z_score(concat_clips)` without the required
    `axis` argument, so the (non-shuffle) concat flow raises TypeError. Pins the broken behavior."""
    df = pd.DataFrame(np.arange(28 * 3, dtype=float).reshape(3, 28))
    with pytest.raises(TypeError):
        ConcatFmriTemporalRelationalCoding()._correlate_concatenated_signals(df)

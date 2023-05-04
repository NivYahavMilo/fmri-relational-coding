import numpy as np
import pandas as pd


def z_score(seq: np.array) -> np.array:
    """
    Computes the Z-score normalization of a given sequence.

    Parameters:
    seq (numpy array): Input sequence to normalize.

    Returns:
    numpy array: Normalized sequence.
    """
    # Compute the Z-score normalization
    seq = (1 / np.std(seq)) * (seq - np.mean(seq))
    return seq


def pearson_correlation(seq: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the pairwise Pearson correlation coefficients for a given DataFrame.

    Parameters:
    seq (pandas DataFrame): Input DataFrame to compute correlations.

    Returns:
    pandas DataFrame: Pairwise Pearson correlation coefficients.
    """
    # Compute the pairwise Pearson correlation coefficients
    corr = (1 / (len(seq) - 1)) * (seq.T @ seq)
    return corr


def ssmd(x_mean, x_std, y_mean, y_std):
    """
    Computes the Strictly Standardized Mean Difference (SSMD) between two groups.

    Parameters:
    x (array-like): Group 1 data.
    y (array-like): Group 2 data.

    Returns:
    ssmd (float): The Strictly Standardized Mean Difference (SSMD) between the two groups.
    """
    ssmd_score = 0
    for a, b, c, d in zip(x_mean, y_mean, x_std, y_std):
        mean_diff = a - b
        pooled_std = np.sqrt(c ** 2 + d ** 2)
        ssmd_value = mean_diff / pooled_std
        ssmd_score += ssmd_value
    return ssmd_score

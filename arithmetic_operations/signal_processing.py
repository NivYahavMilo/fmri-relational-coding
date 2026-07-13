import numpy as np
import pandas as pd
from scipy.signal import welch, filtfilt, butter


class SignalProcessing:

    @staticmethod
    def _get_max_frequency(data: pd.DataFrame):
        values: np.array = data.values

        # calculate the power spectral density (PSD) using the Welch method
        fs = 1.0  # sampling frequency (1 TR = 1 Sec)
        f, psd = welch(values, fs=fs, nperseg=28, scaling='density', axis=1)

        # the frequency carrying the most power (averaged across the signals)
        mean_psd = np.mean(psd, axis=0)
        max_power_freq = abs(f[np.argmax(mean_psd)])

        return round(float(max_power_freq), 3)

    @classmethod
    def low_pass_filtering(cls, data: pd.DataFrame, filter_order: int, cut_off: float):
        max_power_freq = cls._get_max_frequency(data)

        # define the filter parameters
        fs = 1.0  # sampling frequency
        # create the filter coefficients
        nyquist = 0.5 * fs
        # create the filter coefficients
        cutoff_norm = cut_off / nyquist
        b, a = butter(filter_order, cutoff_norm, btype='low', analog=False, output='ba')

        # apply the filter to each column (feature) of the matrix
        filtered_data = np.zeros_like(data)
        for i in range(data.shape[1]):
            filtered_data[:, i] = filtfilt(b, a, data.iloc[:, i])
            data.iloc[:, i].plot()
            import matplotlib.pyplot as plt
            plt.show()
            pd.DataFrame(filtered_data[:, i]).plot()
            plt.show()

        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.columns = data.columns
        return filtered_data

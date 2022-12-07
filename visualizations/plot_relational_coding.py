import os

import numpy as np
import matplotlib.pyplot as plt
import config
import data_normalizer.utils as utils

from enums import Network

def plot_error_bar(data, roi):
    plt.errorbar([*range(19)],
                 data['mean'],
                 data['std']
                 )

    plt.title(f"Mean and Standard deviation of {roi}")
    plt.xlabel("Rest TR")
    plt.ylabel("Correlation Value")

    plt.show()

def gather_subjects_results(roi_name):
    res_path = config.FMRI_RELATION_CODING_RESULTS
    data = utils.load_pkl(f"{res_path}\\{roi_name}.pkl")
    rc_matrix = np.zeros((len(data), 19))
    ii=0
    for sub,l in data.items():

        rc_matrix[ii, :] += l
        ii+=1
    return rc_matrix

def plot_pipe(roi):
    rc_mat = gather_subjects_results(roi)
    rc_stats = {}
    rc_stats['mean'] = np.mean(rc_mat, axis=0)
    rc_stats['std'] = np.std(rc_mat, axis=0,ddof=1) // np.sqrt(rc_mat.shape[0])
    plot_error_bar(rc_stats, roi)

def plot_pipe_single_subject(roi, subject):
    res_path = config.FMRI_RELATION_CODING_RESULTS
    data = utils.load_pkl(f"{res_path}\\{roi}.pkl")
    sub_data = data[subject]
    plt.plot(sub_data)
    plt.title(f"Mean and Standard deviation of {roi}")
    plt.xlabel("Rest TR")
    plt.ylabel("Correlation Value")
    plt.show()

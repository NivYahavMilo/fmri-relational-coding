import os

import numpy as np
import pandas as pd

import config
from enums import AnalysisType

RESULTS_DIR = {
    AnalysisType.ACTIVATIONS_PATTERNS: config.CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG,
    AnalysisType.RELATIONAL_CODING: config.SNR_RELATIONAL_CODING_RESULTS,
    AnalysisType.RESTING_STATE_RELATIONAL_CODING: config.SNR_RESTING_STATE_RELATIONAL_CODING_RESULTS,
    AnalysisType.RESTING_STATE_ACTIVATIONS_PATTERNS: config.CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG,
    AnalysisType.SINGLE_MOVIE_ACTIVATION: config.FMRI_SINGLE_MOVIE_ACTIVATIONS_PATTERN_RESULTS,
    AnalysisType.MOVIE_DISTANCES: config.MOVIE_DISTANCES_CORRELATION_ANALYSIS

}


def gather_dynamic_correlation_by_window(
        n_subjects: int,
        groups: iter,
        roi: str,
        init_window: str,
        init_window_start: int,
        init_window_end: int,
        analysis_mode: AnalysisType
):
    global RESULTS_DIR
    results_path = RESULTS_DIR.get(analysis_mode)

    groups_dict = {}
    for group in groups:

        task_range = 10
        w_s = init_window_start
        w_e = init_window_end

        rc_score = {}
        while w_e < 19:
            _range = f'task_{init_window}_{task_range}_tr_rest_{w_s}-{w_e}_tr'
            res_path = results_path.format(group_amount=n_subjects, group_index=group, range=_range)
            roi_path = os.path.join(res_path, f"{roi}.pkl")
            data = pd.read_pickle(roi_path)

            rc_score[f'{w_s}-{w_e}'] = data.get('relational_coding_distance', data.get('activation_pattern'))
            # rc_score[f'{w_s}-{w_e}'] = data

            w_s += 1
            w_e += 1

        groups_dict[group] = rc_score

    return groups_dict


def add_shuffle(**kwargs):
    kwargs['init_window'] = 'shuffle'
    group_res = gather_dynamic_correlation_by_window(**kwargs)
    correlation_values = 14
    y = np.zeros(shape=(correlation_values, len(group_res)))
    for group_index, dynamic_dict in group_res.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]

    mean_dynamic = y.mean(axis=1)
    std_dynamic = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])
    return y, mean_dynamic, std_dynamic


def get_average_and_std_of_group_dynamics(group_dynamic: dict, correlation_values: int):
    legend = ''
    x_ticks = []
    y = np.zeros(shape=(correlation_values, len(group_dynamic)))
    for group_index, dynamic_dict in group_dynamic.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]
        legend += str(group_index)
        x_ticks = [*dynamic_dict.keys()]

    return y, legend, x_ticks


def create_result_matrix_to_csv(**kwargs):
    groups_results = gather_dynamic_correlation_by_window(**kwargs)
    y, *_ = get_average_and_std_of_group_dynamics(groups_results, correlation_values=14)
    mean_dynamic = y.mean(axis=1)
    std_dynamic = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])

    pass

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config
from enums import AnalysisType

RESULTS_DIR = {
    AnalysisType.ACTIVATIONS_PATTERNS: config.CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG,
    AnalysisType.RELATIONAL_CODING: config.SNR_RELATIONAL_CODING_RESULTS
}


def gather_dynamic_correlation_by_window(
        n_subjects: int,
        groups: iter,
        roi: str,
        init_window: str,
        analysis_mode: AnalysisType
):
    global RESULTS_DIR
    results_path = RESULTS_DIR.get(analysis_mode)

    groups_dict = {}
    for group in groups:

        task_range = 10
        w_s = 0
        w_e = 5

        rc_score = {}
        while w_e < 19:
            _range = f'task_{init_window}_{task_range}_tr_rest_{w_s}-{w_e}_tr'
            res_path = results_path.format(group_amount=n_subjects, group_index=group, range=_range)
            roi_path = os.path.join(res_path, f"{roi}.pkl")
            data = pd.read_pickle(roi_path)
            data_key = 'relational_coding_distance' if analysis_mode == AnalysisType.RELATIONAL_CODING else 'activation_pattern'
            rc_score[f'{w_s}-{w_e}'] = data[data_key]

            w_s += 1
            w_e += 1

        groups_dict[group] = rc_score

    return groups_dict


def plot_groups_roi_dynamic(**kwargs):
    groups_results = gather_dynamic_correlation_by_window(**kwargs)

    legend = ''
    correlation_values = 14
    y = np.zeros(shape=(correlation_values, len(groups_results)))
    for group_index, dynamic_dict in groups_results.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]
        legend += str(group_index)

    sns.set()
    sns.set_theme(style="darkgrid")

    x_ticks = [*dynamic_dict.keys()]
    plt.plot(y)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45)
    plt.ylim([-.4, .8])
    plt.legend(legend)
    plt.title(f"groups dynamic over {kwargs.get('n_subjects')} average subjects\n ROI={kwargs.get('roi')}")
    plt.show()


def plot_mean_and_error_bar_of_group_dynamic(**kwargs):
    groups_results = gather_dynamic_correlation_by_window(**kwargs)
    correlation_values = 14
    y = np.zeros(shape=(correlation_values, len(groups_results)))
    for group_index, dynamic_dict in groups_results.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]
        x_ticks = [*dynamic_dict.keys()]

    mean_dynamic = y.mean(axis=1)
    std_dynamic = y.std(axis=1)

    sns.set()
    sns.set_theme(style="darkgrid")
    plt.plot(range(0, len(mean_dynamic)), mean_dynamic, linewidth=4, color='red')
    plt.fill_between(x=range(0, len(mean_dynamic)),
                     y1=np.array(mean_dynamic) + np.array(std_dynamic),
                     y2=np.array(mean_dynamic) - np.array(std_dynamic),
                     facecolor='gray',
                     alpha=0.5)
    plt.title(f"Mean groups dynamic over {kwargs.get('n_subjects')} average subjects\n ROI={kwargs.get('roi')}")
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45)
    plt.ylim([-1, .8])
    plt.xlabel('Rest TR window')
    plt.ylabel('Correlation Value')
    plt.show()

    # sns.lineplot(x="timepoint", y="signal",
    #              hue="region", style="event",
    #              data='')


if __name__ == '__main__':
    plot_groups_roi_dynamic(
        roi='RH_Default_pCunPCC_1',
        n_subjects=35,
        groups=range(1, 7),
        init_window='end',
        analysis_mode=AnalysisType.ACTIVATIONS_PATTERNS
    )

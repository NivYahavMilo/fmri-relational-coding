import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config
from arithmetic_operations.correlation_and_standartization import ssmd
from data_center.static_data.static_data import StaticData
from enums import AnalysisType
from visualizations.viusalization_utils import gather_dynamic_correlation_by_window, RESULTS_DIR

StaticData.inhabit_class_members()


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
    # plt.ylim([-.8, .8])
    plt.legend(legend)
    plt.title(f"groups dynamic over {kwargs.get('n_subjects')} average subjects\n ROI={kwargs.get('roi')}")
    plt.show()


def plot_mean_and_error_bar_of_group_dynamic(**kwargs):
    roi = kwargs.get('roi')
    figures_path = kwargs.pop('figures_path', '')
    save_fig_path = os.path.join(figures_path, kwargs.get('init_window'), f'{roi}.png')
    if os.path.isfile(save_fig_path):
        return

    with_shuffle = kwargs.pop('add_noise', False)
    if with_shuffle:
        _, mean_shuffle, std_shuffle = add_shuffle(**kwargs)

    correlation_values = kwargs.pop('dynamic_size')
    groups_results = gather_dynamic_correlation_by_window(**kwargs)

    y = np.zeros(shape=(correlation_values, len(groups_results)))
    for group_index, dynamic_dict in groups_results.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]
        x_ticks = [*dynamic_dict.keys()]

    y = np.nan_to_num(y)
    mean_dynamic = y.mean(axis=1)
    std_dynamic = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])

    sns.set()
    sns.set_theme(style="darkgrid")
    fig = plt.gcf()
    plt.plot(range(0, len(mean_dynamic)), mean_dynamic, linewidth=4, color='blue')
    if with_shuffle:
        plt.plot(range(0, len(mean_shuffle)), mean_shuffle, linewidth=2, color='gold')
        plt.fill_between(x=range(0, len(mean_shuffle)),
                         y1=np.array(mean_shuffle) + np.array(std_shuffle),
                         y2=np.array(mean_shuffle) - np.array(std_shuffle),
                         facecolor='gold',
                         alpha=0.2)

    plt.fill_between(x=range(0, len(mean_dynamic)),
                     y1=np.array(mean_dynamic) + np.array(std_dynamic),
                     y2=np.array(mean_dynamic) - np.array(std_dynamic),
                     facecolor='blue',
                     alpha=0.2)

    title = f"Mean of 6 groups dynamic over 29-30 average subjects\n ROI={kwargs.get('roi')}\nCLIP_WINDOW={kwargs.get('init_window').replace('dynamic', '')}TR"
    plt.title(title)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45)
    plt.ylim([-.4, .9])
    plt.xlabel('Rest TR window')
    plt.ylabel('Correlation Value')
    plt.legend([kwargs.get('analysis_mode').value, 'shuffle'])

    plt.draw()
    plt.show()
    if not os.path.isfile(save_fig_path):
        fig.savefig(save_fig_path, dpi=300)


def add_shuffle(dynamic_size: int, **kwargs):
    kwargs['init_window'] = 'shuffle'
    group_res = gather_dynamic_correlation_by_window(**kwargs)
    y = np.zeros(shape=(dynamic_size, len(group_res)))
    for group_index, dynamic_dict in group_res.items():
        y[:, group_index - 1] = [*dynamic_dict.values()]

    mean_dynamic = y.mean(axis=1)
    std_dynamic = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])
    return y, mean_dynamic, std_dynamic


def save_all_figures_flow():
    for roi in StaticData.ROI_NAMES:
        for window in ['start', 'middle', 'end']:
            for analysis, path_ in zip(RESULTS_DIR.keys(), [config.ARTICLE_FIGURES_PATH_ACTIVATIONS,
                                                            config.ARTICLE_FIGURES_PATH_CORRELATIONS]):
                plot_mean_and_error_bar_of_group_dynamic(
                    roi=roi,
                    n_subjects=35,
                    groups=range(1, 7),
                    init_window=window,
                    add_noise=True,
                    analysis_mode=analysis,
                    figures_path=path_

                )


def create_bar_plot_with_ssdm_measurement(**kwargs):
    roi_to_net = {}
    ssmd_results = {}
    with_shuffle = kwargs.pop('add_noise', False)
    dynamic_size = kwargs.pop('dynamic_size')
    for roi in StaticData.ROI_NAMES:
        kwargs['roi'] = roi

        if with_shuffle:
            y_shuffle, mean_shuffle, std_shuffle = add_shuffle(dynamic_size, **kwargs)

        groups_results = gather_dynamic_correlation_by_window(**kwargs)
        y = np.zeros(shape=(dynamic_size, len(groups_results)))
        for group_index, dynamic_dict in groups_results.items():
            y[:, group_index - 1] = [*dynamic_dict.values()]

        mean_dynamic = y.mean(axis=1)
        std_dynamic = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])
        ssmd_value = ssmd(mean_dynamic, std_dynamic, mean_shuffle, std_shuffle)
        ssmd_results[roi] = ssmd_value

    networks = {'Default': 'default', 'Visual': 'vis', 'Frontoparietal': 'cont', 'Somatomotor': 'sommot',
                'DorsalAttention': 'dors', 'Limbic': 'limbic', 'VentralAttention': 'sal'}
    for net_name, net_alias in networks.items():
        for roi in ssmd_results.keys():
            if re.search(fr'{net_alias}', roi, re.I):
                roi_to_net[roi] = net_name

    network_colors = {'Default': 'blue', 'Visual': 'green', 'DorsalAttention': 'red',
                      'Limbic': 'orange', 'VentralAttention': 'purple', 'Frontoparietal': 'brown',
                      'Somatomotor': 'gray'}

    sns.set()
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(30, 15))
    fig = plt.gcf()

    # Sort the dictionary by ROI values in ascending order
    sorted_roi_values = sorted(ssmd_results.items(), key=lambda x: x[1], reverse=True)

    # Extract the sorted ROI names and values
    sorted_rois = [x[0] for x in sorted_roi_values]
    sorted_values = [x[1] for x in sorted_roi_values]

    # Create a list of colors for each ROI based on its network
    roi_colors = [network_colors[roi_to_net[roi]] for roi in sorted_rois]

    # Create a bar plot with colored bars for each network
    plt.bar(range(len(sorted_values)), sorted_values, color=roi_colors)

    # Create bar chart with network colors and legend
    # fig, ax = plt.subplots()
    # bars = ax.bar(x_values, y_values, color=network_colors)

    # Create legend for network colors
    networks_unique = list(network_colors.keys())
    colors = list(network_colors.values())
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]

    legend = plt.legend(handles, networks_unique, title='Network', bbox_to_anchor=(1.05, 1), loc='upper left')
    legend.get_frame().set_linewidth(1.5)
    legend.legendHandles[0]._sizes = [50]

    # Add x-axis and y-axis labels
    plt.xlabel('ROI', fontweight='bold')
    plt.ylabel('SSMD Value', fontsize=20, fontweight='bold')
    # Set title and font size
    title = f'Strictly standardized mean difference of the {kwargs.get("init_window").title()} movie part'
    plt.title(title, fontsize=40, fontweight='bold')

    # Add tick labels
    plt.xticks(range(len(sorted_rois)), sorted_rois, rotation=90, fontsize=6, fontweight='bold')
    # Set font size of y-axis tick labels
    plt.yticks(fontsize=30, fontweight='bold')

    plt.draw()
    plt.show()
    fig.savefig(f'{title}.png', dpi=300, bbox_inches='tight', pad_inches=0.5)


if __name__ == '__main__':
    #     for roi in StaticData.ROI_NAMES:
    #         plot_groups_roi_dynamic(
    #             roi=roi,
    #             n_subjects='35',
    #             groups=range(1, 7),
    #             init_window='end',
    #             init_window_start=0,
    #             init_window_end=5,
    #             analysis_mode=AnalysisType.RESTING_STATE_RELATIONAL_CODING
    #             # figures_path=config.SNR_RESTING_STATE_RELATIONAL_CODING_RESULTS_FIGURES
    #         )
    for roi in StaticData.ROI_NAMES:
        plot_mean_and_error_bar_of_group_dynamic(
            roi='RH_DorsAttn_Post_2',
            n_subjects='35',
            groups=range(1, 7),
            init_window='end',
            init_window_start=0,
            init_window_end=5,
            dynamic_size=14,
            add_noise=False,
            analysis_mode=AnalysisType.MOVIE_DISTANCES,
            figures_path=''
        )
        break

    # for window in ['end', 'start', 'middle']:
    #     create_bar_plot_with_ssdm_measurement(
    #         n_subjects='35',
    #         groups=range(1, 7),
    #         init_window=window,
    #         init_window_start=2,
    #         init_window_end=7,
    #         dynamic_size=12,
    #         add_noise=True,
    #         analysis_mode=AnalysisType.RELATIONAL_CODING

    # figures_path=config.ARTICLE_FIGURES_PATH_CORRELATIONS

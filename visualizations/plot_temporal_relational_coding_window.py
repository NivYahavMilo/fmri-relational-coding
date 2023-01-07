import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
from data_center.static_data.static_data import StaticData


def window_relational_coding_plot(show=True, save_img=False):
    if not getattr(StaticData, 'ROI_NAMES'):
        StaticData.inhabit_class_members()
    task_window = 10
    w_s = 0
    w_e = 5

    for roi in StaticData.ROI_NAMES:
        mean_roi = []
        std_roi = []
        rest_windows = []
        while w_e < 19:

            results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS.format(
                range=f'task_{task_window}_rest{w_s}-{w_e}')
            res_path = os.path.join(results_path, f"{roi}.pkl")
            data = pd.read_pickle(res_path)
            rc_values = pd.Series(list(data.values()))
            rc_mean = round(rc_values.values.mean(), 2)
            rc_std = round(rc_values.values.std(), 2)
            mean_roi.append(rc_mean)
            std_roi.append(rc_std)
            rest_windows.append((w_s,w_e))

            w_s += 1
            w_e += 1

        w_s = 0
        w_e = 5
        plt.plot(range(0, len(mean_roi)), mean_roi, linewidth=3)
        plt.fill_between(x=range(0, len(mean_roi)),
                         y1=np.array(mean_roi) + np.array(std_roi),
                         y2=np.array(mean_roi) - np.array(std_roi),
                         facecolor='yellow',
                         alpha=0.5)
        plt.title(f"moving relational coding average window\n{roi}")
        plt.xticks(np.arange(len(rest_windows)),rest_windows, rotation=45)
        plt.ylim([-0.2, 0.3])
        plt.xlabel("Mean window range Value")
        fig1 = plt.gcf()
        if show:
            plt.show()
        if save_img:
            figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES

            plt.draw()
            fig1.savefig(os.path.join(figure_path, f'{roi}.png'), dpi=100)


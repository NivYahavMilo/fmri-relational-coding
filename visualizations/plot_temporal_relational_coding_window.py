import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
from data_center.static_data.static_data import StaticData


def window_relational_coding_plot(task_window, show=True, save_img=False, avg_data=False):
    if not getattr(StaticData, 'ROI_NAMES'):
        StaticData.inhabit_class_members()

    if avg_data:
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_AVG_FIGURES.format(task_window=task_window)
    else:
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES.format(task_window=task_window)
    task_range = 10
    w_s = 0
    w_e = 5

    for roi in StaticData.ROI_NAMES:
        mean_roi = []
        std_roi = []
        rest_windows = []
        while w_e < 19:
            res_path = results_path.format(range=f'task_{task_window}_{task_range}_tr_rest_{w_s}-{w_e}_tr')
            res_path = os.path.join(res_path, f"{roi}.pkl")
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
        plt.ylim([-1,1])
        plt.xlabel("Mean window range Value")
        fig1 = plt.gcf()
        if show:
            plt.show()
        if save_img:


            plt.draw()
            fig1.savefig(os.path.join(figure_path, f'{roi}.png'), dpi=100)


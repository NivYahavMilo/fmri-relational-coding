import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
from data_center.static_data.static_data import StaticData


def plot_snr_measurement():
    if not getattr(StaticData, 'ROI_NAMES'):
        StaticData.inhabit_class_members()

    main_path = config.SNR_RELATIONAL_CODING_RESULTS
    figure_path = config.SNR_RELATIONAL_CODING_RESULTS_FIGURES
    subjects_groups = [5, 10, 15, 20, 25, 30, 40, 50]
    group_index = 2
    roi_mean_score = {}
    task_range = 10
    w_s = 0
    w_e = 5
    for roi in StaticData.ROI_NAMES:
        rc_mean_score = {}
        for group_amount in subjects_groups:
            rc_score = []
            while w_e < 19:
                _range = f'task_end_{task_range}_tr_rest_{w_s}-{w_e}_tr'
                res_path = main_path.format(group_amount=group_amount, group_index=group_index, range=_range)
                roi_path = os.path.join(res_path, f"{roi}.pkl")
                data = pd.read_pickle(roi_path)
                rc_score.append(data['relational_coding_distance'])

                w_s += 1
                w_e += 1

            rc_mean_score[group_amount] = round(np.mean(rc_score), 3)
            w_s = 0
            w_e = 5

        roi_mean_score[roi] = rc_mean_score


    for roi in roi_mean_score.keys():
        plt.plot(roi_mean_score[roi].keys(), roi_mean_score[roi].values(), linewidth=5)
        plt.title(f'SNR Measurement as Subject Group function {roi}')
        plt.xticks(subjects_groups)
        plt.xlabel('Subject Groups')
        plt.ylabel('Average Correlation Window Value')
        plt.ylim([-.8,.8])

        fig1 = plt.gcf()
        plt.show()
        plt.draw()
        save_fig_path = os.path.join(figure_path.format(group_index=group_index), f'{roi}.png')
        fig1.savefig(save_fig_path, dpi=300)

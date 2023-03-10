import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
from data_center.static_data.static_data import StaticData

plt.rcParams["figure.figsize"] = (20,10)
plt.rcParams["font.size"] = 20

def window_average_rc_bar_plot(avg_data, with_shuffle=False, save_img=None):
    if avg_data:
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_AVG_FIGURES
    else:
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES

    n_windows = 14
    n_subjects = 176
    roi_section = {}
    for section in ['start', 'middle', 'end']:
        roi_section[section] = {}
        task_range = 10
        w_s = 0
        w_e = 5
        for roi in StaticData.ROI_NAMES:
            window_avg_value = np.zeros((n_windows, n_subjects))
            while w_e < 19:
                res_path = results_path.format(range=f'task_{section}_{task_range}_tr_rest{w_s}-{w_e}_tr')
                res_path = os.path.join(res_path, f"{roi}.pkl")
                data = pd.read_pickle(res_path)
                window_avg_value[w_s, :] += list(data.values())
                w_s += 1
                w_e += 1

            roi_section[section][roi] = np.mean(window_avg_value)# np.max(np.mean(window_avg_value,axis=1))
            w_s = 0
            w_e = 5

    if with_shuffle and avg_data:
        roi_section['shuffle'] = {}
        for roi in StaticData.ROI_NAMES:
            res_path = os.path.join(config.FMRI_RELATION_CODING_SHUFFLE_REST_RESULTS, f"{roi}.pkl")
            data = pd.read_pickle(res_path)
            mean_rc = np.mean(data['avg'])
            roi_section['shuffle'][roi] = mean_rc


    networks = {'Visual': 'vis', 'Default': 'default', 'Frontoparietal': 'cont', 'Somatomotor': 'sommot',
                'DorsalAttention': 'dors', 'Limbic': 'limbic', 'VentralAttention': 'sal'}
    for net_name, net_alias in networks.items():
        net_roi = [r for r in StaticData.ROI_NAMES if re.search(fr'{net_alias}', r, re.I)]
        X_axis = np.arange(len(net_roi))
        end, mid, start, shuffle = [], [], [], []
        for r in net_roi:
            end.append(roi_section['end'][r])
            mid.append(roi_section['middle'][r])
            start.append(roi_section['start'][r])
            # shuffle.append(roi_section['shuffle'][r])


        plt.bar(X_axis - .2, end, 0.3, label='end clip', color='red')
        plt.bar(X_axis, mid, 0.3, label='middle clip', color='green')
        plt.bar(X_axis + 0.2, start, 0.3, label='start clip', color='cyan')
        if with_shuffle and avg_data:
            plt.bar(X_axis + 0.4, shuffle, 0.3, label='shuffle clip', color='black')

        plt.xticks(X_axis, net_roi, rotation=90, fontsize=6)
        plt.xlabel("ROI")
        plt.ylabel("Averaged Relational Coding")
        plt.title(f"3 Clip Section Relational Coding Mean Dynamic Value {net_name}")
        plt.legend()
        fig1 = plt.gcf()
        plt.show()
        if save_img:
            plt.draw()
            fig1.savefig(os.path.join(figure_path.format(task_window='_conclusion'), f'{net_name}.png'), dpi=300)


def window_relational_coding_plot(task_window, mode=None, **kwargs):
    if not getattr(StaticData, 'ROI_NAMES'):
        StaticData.inhabit_class_members()

    if kwargs.get('avg_data'):
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_AVG_FIGURES.format(task_window=task_window)

    elif mode=='pca':
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_PCA
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_PCA_FIGURES.format(task_window=task_window)

    elif mode =='filtering':
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_FILTERING
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_FILTERING_FIGURES.format(task_window=task_window)

    else:
        results_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS
        figure_path = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES.format(task_window=task_window)
    task_range = 10
    w_s = 0
    w_e = 5

    if kwargs.get('roi'):
        rois = kwargs.pop('roi')
    else:
        rois = [roi for roi in StaticData.ROI_NAMES]
    for roi in rois:
        mean_roi = []
        std_roi = []
        rest_windows = []
        while w_e < 30:
            res_path = results_path.format(range=f'task_{task_window}_{task_range}_tr_rest_{w_s}-{w_e}_tr')
            res_path = os.path.join(res_path, f"{roi}.pkl")
            data = pd.read_pickle(res_path)
            rc_values = pd.Series(list(data.values()))
            rc_mean = round(rc_values.values.mean(), 2)
            rc_std = round(rc_values.values.std(), 2)
            mean_roi.append(rc_mean)
            std_roi.append(rc_std)
            rest_windows.append((w_s, w_e))

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
        plt.xticks(np.arange(len(rest_windows)), rest_windows, rotation=45)
        plt.ylim([-1, 1])
        plt.xlabel("Mean window range Value")
        fig1 = plt.gcf()
        if kwargs.get('show'):
            plt.show()
        if kwargs.get('save_img'):
            img_path = os.path.join(figure_path, f'{roi}.png')
            if not os.path.isfile(img_path):
                plt.draw()
                fig1.savefig(img_path, dpi=300)

"""ROI data loading for the relational-coding flows (previously base-class methods)."""
import os

import pandas as pd

import config
from data_center.static_data.static_data import StaticData


def check_roi_validity(roi_name: str):
    if roi_name not in StaticData.ROI_NAMES:
        raise ValueError("ROI name incorrect\n", "check the following list:\n", StaticData.ROI_NAMES)


def load_roi_data(roi_name: str, subject: str, mode):
    check_roi_validity(roi_name)
    data_path = config.SUBNET_DATA_DF.format(mode=mode.value)
    return pd.read_pickle(os.path.join(data_path, subject, f"{roi_name}.pkl"))


def load_avg_data(roi_name: str, mode, group: str = ''):
    check_roi_validity(roi_name)
    data_path = config.SUBNET_DATA_AVG.format(mode=mode.value, group=group)
    return pd.read_pickle(os.path.join(data_path, f"{roi_name}.pkl"))


def load_group_subjects(roi: str, mode, n_subjects: int, group_index: int):
    group_path = config.SUBNET_AVG_N_SUBJECTS.format(mode=mode.value, n_subjects=n_subjects, group_i=group_index)
    return pd.read_pickle(os.path.join(group_path, f'{roi}.pkl'))

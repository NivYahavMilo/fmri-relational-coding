"""Inter-subject functional correlation relational coding (was ISFCRelationalCoding)."""
import os

import pandas as pd

import config
import data_access
import rc_core
from data_center.static_data.static_data import StaticData
from data_normalizer import utils
from enums import Mode


def _load_subjects_average_leave_one_out(roi_name, subject):
    data_path = os.path.join(config.SUBJECTS_AVG_DATA_LEAVE_ONE_OUT, subject, f"{roi_name}.pkl")
    return pd.read_pickle(data_path)


def _isfc_relational_coding(data_task, data_rest, window_size_task, shuffle):
    subjects_avg_data = {}
    sub_rc_dis = []
    for rest_tr in rc_core.rest_between_tr_generator():
        for clip_index in range(1, 15):
            clip_name = rc_core.get_clip_name_by_index(clip_index)
            subjects_avg_data[clip_name + '_task'] = rc_core.get_task_window_slides_vectors(
                data_task=data_task, clip_i=clip_index, init_window='end', window_size_task=window_size_task)
            subjects_avg_data[clip_name + '_rest'] = rc_core.get_single_tr_vector(
                data=data_rest, clip_i=clip_index, timepoint=rest_tr)
        rc_distance, _ = rc_core.correlate_current_timepoint(data=subjects_avg_data, shuffle_rest=shuffle)
        sub_rc_dis.append(rc_distance)
    return sub_rc_dis


def run(roi):
    results_path = os.path.join(config.ISFC_RELATIONAL_CODING_RESULTS, f"{roi}.pkl")
    if os.path.isfile(results_path):
        return

    subject_result = {}
    for subject in StaticData.SUBJECTS:
        subject_task_data = data_access.load_roi_data(roi_name=roi, subject=subject, mode=Mode.CLIPS)
        rest_subjects_data = _load_subjects_average_leave_one_out(roi_name=roi, subject=subject)
        subject_result[subject] = _isfc_relational_coding(
            data_task=subject_task_data, data_rest=rest_subjects_data, window_size_task=10, shuffle=False)
    utils.dict_to_pkl(subject_result, results_path.replace('.pkl', ''))

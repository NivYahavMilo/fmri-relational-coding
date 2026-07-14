"""Per-subject / averaged relational coding across the rest timepoints (was FmriRelationalCoding)."""
import os

import config
import data_access
import data_normalizer.utils as utils
import rc_core
from enums import Mode


def _get_clip_vectors(rest_data, task_data, timepoint):
    tr_vec = {}
    for clip_i in range(1, 15):
        clip_name = rc_core.get_clip_name_by_index(clip_i)
        tr_vec[clip_name + '_task'] = rc_core.get_single_tr_vector(data=task_data, clip_i=clip_i)
        tr_vec[clip_name + '_rest'] = rc_core.get_single_tr_vector(data=rest_data, clip_i=clip_i, timepoint=timepoint)
    return tr_vec


def _relation_distance(d_rest, d_task, shuffle):
    sub_rc_dis, sub_rc_corr = [], []
    for tr in rc_core.rest_between_tr_generator():
        clip_matrix = _get_clip_vectors(rest_data=d_rest, task_data=d_task, timepoint=tr)
        rc_distance, corr_df = rc_core.correlate_current_timepoint(data=clip_matrix, shuffle_rest=shuffle)
        sub_rc_dis.append(rc_distance)
        sub_rc_corr.append(corr_df)
    return sub_rc_dis, sub_rc_corr


def _avg_data_flow(roi, res_path, group, shuffle):
    data = {}
    roi_avg_task = data_access.load_avg_data(roi_name=roi, mode=Mode.CLIPS, group=group)
    roi_avg_rest = data_access.load_avg_data(roi_name=roi, mode=Mode.REST, group=group)
    sub_rc_dis, df_corr = _relation_distance(d_rest=roi_avg_rest, d_task=roi_avg_task, shuffle=shuffle)
    data['avg'] = sub_rc_dis
    data['avg correlation'] = df_corr
    utils.dict_to_pkl(data, res_path.replace('.pkl', ''))
    print(f'Saved roi {roi}')


def _subject_flow(roi, res_path, shuffle):
    data = {}
    for sub_id in rc_core.subjects_generator():
        roi_sub_data_task = data_access.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
        roi_sub_data_rest = data_access.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)
        sub_rc_dis, _ = _relation_distance(d_rest=roi_sub_data_rest, d_task=roi_sub_data_task, shuffle=shuffle)
        data[sub_id] = sub_rc_dis
    utils.dict_to_pkl(data, res_path.replace('.pkl', ''))
    print(f'Saved roi {roi}')


def run(roi, avg_data=False, group='', shuffle=False):
    if avg_data:
        save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS_AVG.format(group=group.lower()), f"{roi}.pkl")
        if shuffle:
            save_path = os.path.join(config.FMRI_RELATION_CODING_SHUFFLE_REST_RESULTS, f"{roi}.pkl")
            if os.path.isfile(save_path):
                return
        _avg_data_flow(roi, save_path, group, shuffle)
    else:
        save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS, f"{roi}.pkl")
        if shuffle:
            save_path = os.path.join(config.FMRI_RELATION_CODING_SHUFFLE_REST_RESULTS, f"{roi}.pkl")
            if os.path.isfile(save_path):
                return
        _subject_flow(roi, save_path, shuffle)

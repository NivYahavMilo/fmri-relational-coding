"""Singular relational coding: task end-TR vs averaged rest per clip (was SingularRelationalCoding)."""
import os

import config
import data_access
import rc_core
from data_normalizer import utils
from enums import Mode


def run(roi, group=''):
    save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS, f"{roi}.pkl")
    if os.path.isfile(save_path):
        return
    data = {}
    for sub_id in rc_core.subjects_generator():
        roi_sub_data_task = data_access.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
        roi_sub_data_rest = data_access.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)
        data[sub_id] = rc_core.singular_relational_coding(d_rest=roi_sub_data_rest, d_task=roi_sub_data_task)
    utils.dict_to_pkl(data, save_path.replace('.pkl', ''))
    print(f'Saved roi {roi}')

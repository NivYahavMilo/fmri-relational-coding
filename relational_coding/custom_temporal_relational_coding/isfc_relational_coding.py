import os

import numpy as np
import pandas as pd

import config
from data_center.static_data.static_data import StaticData
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import \
    CustomTemporalRelationalCodingUtils
from relational_coding.relational_coding_base import RelationalCodingBase


class ISFCRelationalCoding(RelationalCodingBase, CustomTemporalRelationalCodingUtils):

    def __isfc_relational_coding(self, data_task, data_rest, window_size_task, shuffle):
        subjects_avg_data = {}

        sub_rc_dis = []
        sub_rc_corr = []
        for rest_tr in self.rest_between_tr_generator():


            for clip_index in range(1, 15):
                clip_name = self.get_clip_name_by_index(clip_index)

                subject_clip_avg_vector = self.get_task_window_slides_vectors(
                    data_task=data_task,
                    clip_i=clip_index,
                    init_window='end',
                    window_size_task=window_size_task
                )
                subjects_avg_data[clip_name + '_task'] = subject_clip_avg_vector

                remaining_subject_rest_avg_vector = []
                for sub_rest_data in data_rest:
                    remaining_subject_rest_avg_vector.append(
                        self.get_single_tr_vector(sub_rest_data, clip_index, rest_tr))

                remaining_subject_rest_avg_vector = np.mean(remaining_subject_rest_avg_vector, axis=0)
                subjects_avg_data[clip_name + '_rest'] = remaining_subject_rest_avg_vector

            rc_distance, _ = self.correlate_current_timepoint(data=subjects_avg_data, shuffle_rest=shuffle)
            sub_rc_dis.append(rc_distance)

        return sub_rc_dis

    def run(self, roi: str, *args, **kwargs):
        results_path = os.path.join(config.ISFC_RELATIONAL_CODING_RESULTS,  f"{roi}.pkl")
        if os.path.isfile(results_path):
            return

        subject_result = {}

        for subject in StaticData.SUBJECTS:
            remaining_subjects = StaticData.SUBJECTS.copy()
            remaining_subjects.remove(subject)
            subject_task_data = self.load_roi_data(roi_name=roi, subject=subject, mode=Mode.CLIPS)
            rest_subject_data = []
            for sub in remaining_subjects:
                rest_subject_data.append(self.load_roi_data(roi_name=roi, subject=sub, mode=Mode.REST))

            rc_distance = self.__isfc_relational_coding(
                data_task=subject_task_data,
                data_rest=rest_subject_data,
                window_size_task=10,
                shuffle=False)

            subject_result[subject] = rc_distance

        utils.dict_to_pkl(subject_result, results_path.replace('.pkl', ''))

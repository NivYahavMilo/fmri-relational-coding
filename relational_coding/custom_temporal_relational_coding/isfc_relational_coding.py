import os

import pandas as pd

import config
from data_center.static_data.static_data import StaticData
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import CustomTemporalRelationalCodingUtils


class ISFCRelationalCoding(CustomTemporalRelationalCodingUtils):

    def __isfc_relational_coding(self, data_task, data_rest, window_size_task, shuffle):
        subjects_avg_data = {}

        sub_rc_dis = []
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

                subject_rest_avg_vector = self.get_single_tr_vector(
                    data=data_rest,
                    clip_i=clip_index,
                    timepoint=rest_tr
                )
                subjects_avg_data[clip_name + '_rest'] = subject_rest_avg_vector

            rc_distance, _ = self.correlate_current_timepoint(data=subjects_avg_data, shuffle_rest=shuffle)
            sub_rc_dis.append(rc_distance)

        return sub_rc_dis

    @staticmethod
    def _load_subjects_average_with_leave_one_out(roi_name, subject):
        data_path = os.path.join(config.SUBJECTS_AVG_DATA_LEAVE_ONE_OUT, subject, f"{roi_name}.pkl")
        data = pd.read_pickle(data_path)
        return data

    def run(self, roi: str, *args, **kwargs):
        results_path = os.path.join(config.ISFC_RELATIONAL_CODING_RESULTS, f"{roi}.pkl")
        if os.path.isfile(results_path):
            return

        subject_result = {}

        for subject in StaticData.SUBJECTS:
            subject_task_data = self.load_roi_data(roi_name=roi, subject=subject, mode=Mode.CLIPS)
            rest_subjects_data = self._load_subjects_average_with_leave_one_out(roi_name=roi, subject=subject)

            rc_distance = self.__isfc_relational_coding(
                data_task=subject_task_data,
                data_rest=rest_subjects_data,
                window_size_task=10,
                shuffle=False)

            subject_result[subject] = rc_distance

        utils.dict_to_pkl(subject_result, results_path.replace('.pkl', ''))

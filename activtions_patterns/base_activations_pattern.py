import os
from abc import abstractmethod

import pandas as pd

import config
from data_center.static_data.static_data import StaticData
from enums import Mode


class BaseActivationPattern:

    @staticmethod
    def rest_between_tr_generator():
        for i in range(19):
            yield i

    def get_clip_vectors(self, rest_data, task_data, timepoint):
        tr_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)

            task_vector = self.get_single_tr_vector(data=task_data, clip_i=clip_i)
            tr_vec[clip_name + '_task'] = task_vector

            rest_vector = self.get_single_tr_vector(data=rest_data, clip_i=clip_i, timepoint=timepoint)
            tr_vec[clip_name + '_rest'] = rest_vector

        return tr_vec

    @staticmethod
    def get_single_tr_vector(data: pd.DataFrame, clip_i: int, timepoint: int = -1):
        if timepoint == -1:
            xdf = data[data['y'] == clip_i]
            timepoint = int(max(xdf['timepoint'].values))

        sequence = data[(data['timepoint'] == timepoint) &
                        (data['y'] == clip_i)]

        sequence = sequence.drop(['y', 'timepoint'], axis=1)

        return sequence.values[0].tolist()

    @staticmethod
    def rearrange_clip_order(df):
        clip_order = StaticData.CLIPS_ORDER + StaticData.REST_ORDER
        df = df[clip_order]
        return df

    @staticmethod
    def get_clip_name_by_index(i):
        return StaticData.CLIP_MAPPING.get(str(i))

    def load_avg_data(self, roi_name: str, mode: Mode, group: int):
        self._check_roi_validity(roi_name)
        # if pass validity checks
        data_path = config.SUBNET_DATA_AVG.format(mode=mode.value, group=group)
        roi_data_p = os.path.join(data_path, f"{roi_name}.pkl")
        roi_data_df = pd.read_pickle(roi_data_p)
        return roi_data_df

    @staticmethod
    def _check_roi_validity(roi_name: str):
        if roi_name not in StaticData.ROI_NAMES:
            raise ValueError("ROI name incorrect\n", "check the following list:\n", StaticData.ROI_NAMES)

    @staticmethod
    def load_group_data(roi, mode, **kwargs):
        group_index = kwargs.pop('group_index')
        n_subjects = kwargs.pop('n_subjects')
        group_path = config.SUBNET_AVG_N_SUBJECTS.format(mode=mode.value, n_subjects=n_subjects, group_i=group_index)
        roi_path = os.path.join(group_path, f'{roi}.pkl')
        df = pd.read_pickle(roi_path)
        return df

    @abstractmethod
    def run(self, roi: str, *args, **kwargs):
        pass

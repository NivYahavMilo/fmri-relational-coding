import os

import pandas as pd

import config
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import CustomTemporalRelationalCodingUtils


class SnrMeasurementsRelationalCoding(CustomTemporalRelationalCodingUtils):

    @staticmethod
    def _load_group_subjects(roi, mode, **kwargs):
        n_subjects = kwargs.pop('group_subjects')
        group_index = kwargs.pop('group_index')
        group_path = config.SUBNET_AVG_N_SUBJECTS.format(mode=mode.value, n_subjects=n_subjects, group_i=group_index)
        roi_path = os.path.join(group_path, f'{roi}.pkl')
        df = pd.read_pickle(roi_path)
        return df

    def run(self, roi: str, *args, **kwargs):

        init_window_task = kwargs.pop('init_window')
        ws_task = kwargs.pop('task_ws')
        ws_rest = kwargs.pop('rest_ws')

        output_dir = config.SNR_RELATIONAL_CODING_RESULTS.format(
            range=f'task_{init_window_task}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr',
            group_amount=kwargs['group_subjects'],
            group_index=kwargs['group_index']
        )
        save_path = os.path.join(output_dir, f"{roi}.pkl")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.isfile(save_path):
            return

        data = {}
        roi_data_task = self._load_group_subjects(roi=roi, mode=Mode.CLIPS, **kwargs)
        roi_data_rest = self._load_group_subjects(roi=roi, mode=Mode.REST, **kwargs)

        rc_distance = self.custom_temporal_relational_coding(
            data_task=roi_data_task,
            data_rest=roi_data_rest,
            window_size_rest=ws_rest,
            init_window_task=init_window_task,
            window_size_task=ws_task,
            **kwargs
        )

        data['relational_coding_distance'] = rc_distance
        utils.dict_to_pkl(data, save_path.replace('.pkl', ''))

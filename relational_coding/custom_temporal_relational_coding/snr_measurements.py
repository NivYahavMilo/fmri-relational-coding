import os

import config
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import \
    CustomTemporalRelationalCodingUtils


class SnrMeasurementsRelationalCoding(CustomTemporalRelationalCodingUtils):

    def run(self, roi: str, *args, **kwargs):

        init_window_task = kwargs.pop('init_window')
        ws_task = kwargs.pop('task_ws')
        ws_rest = kwargs.pop('rest_ws')

        output_dir = config.MOVIE_DISTANCES_CORRELATION_ANALYSIS.format(
            range=f'task_{init_window_task}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr',
            group_amount=kwargs['group_subjects'],
            group_index=kwargs['group_index']
        )
        save_path = os.path.join(output_dir, f"{roi}.pkl")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # if os.path.isfile(save_path):
        #     return

        data = {}
        roi_data_task = self.load_group_subjects(roi=roi, mode=Mode.CLIPS, **kwargs)
        roi_data_rest = self.load_group_subjects(roi=roi, mode=Mode.REST, **kwargs)

        rc_distance, roi_feature_matrix = self.custom_temporal_relational_coding(
            data_task=roi_data_task,
            data_rest=roi_data_rest,
            window_size_rest=ws_rest,
            init_window_task=init_window_task,
            window_size_task=ws_task,
            **kwargs
        )

        data['relational_coding_distance'] = rc_distance
        # data['feature_matrix'] = roi_feature_matrix
        utils.dict_to_pkl(data, save_path.replace('.pkl', ''))

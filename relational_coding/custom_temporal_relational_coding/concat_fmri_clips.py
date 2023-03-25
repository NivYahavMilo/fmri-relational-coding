import os

import numpy as np
import pandas as pd

import config
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import \
    CustomTemporalRelationalCodingUtils


class ConcatFmriTemporalRelationalCoding(CustomTemporalRelationalCodingUtils):

    @staticmethod
    def _correlate_concatenated_signals(tr_signals_df):
        N_VECTORS = 28
        clips = tr_signals_df.iloc[:, :N_VECTORS:2]
        rest = tr_signals_df.iloc[:, 1:N_VECTORS:2]

        concat_clips = np.concatenate(clips.values)
        concat_rests = np.concatenate(rest.values)

        df_concatenated_signals = pd.DataFrame({'concat_clip': concat_clips, 'concat_rest': concat_rests})
        df_corr = df_concatenated_signals.corr()
        distance = round(df_corr.loc['concat_clip'].at['concat_rest'], 3)

        return distance, df_concatenated_signals

    def run(self, roi: str, *args, **kwargs):
        init_window_task = kwargs.pop('init_window')
        ws_task = kwargs.pop('task_ws')
        ws_rest = kwargs.pop('rest_ws')

        _range = f'task_{init_window_task}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr'

        output_dir = config.CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG.format(
            range=_range,
            group_amount=kwargs['group_subjects'],
            group_index=kwargs['group_index']
        )
        save_path = os.path.join(output_dir, f"{roi}.pkl")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.isfile(save_path):
            return

        roi_data_task = self.load_group_subjects(roi=roi, mode=Mode.CLIPS, **kwargs)
        roi_data_rest = self.load_group_subjects(roi=roi, mode=Mode.REST, **kwargs)

        tr_vectors_df = self.custom_temporal_relational_coding(
            data_task=roi_data_task,
            data_rest=roi_data_rest,
            window_size_rest=ws_rest,
            init_window_task=init_window_task,
            window_size_task=ws_task,
            skip_correlation=True,
            **kwargs
        )

        distance, concat_signals = self._correlate_concatenated_signals(tr_signals_df=tr_vectors_df)

        activation_values = {'activation_pattern': distance, 'concat_signals': concat_signals}

        utils.dict_to_pkl(activation_values, save_path.replace('.pkl', ''))

import os

import numpy as np
import pandas as pd

import config
from arithmetic_operations.correlation_and_standartization import z_score
from data_normalizer import utils
from enums import Mode
from relational_coding.custom_temporal_relational_coding.custom_temporal_rc_utils import \
    CustomTemporalRelationalCodingUtils


class ConcatFmriTemporalRelationalCoding(CustomTemporalRelationalCodingUtils):

    def _correlate_concatenated_signals(self, tr_signals_df, **kwargs):
        N_VECTORS = 28

        if kwargs.get('shuffle_rest'):
            tr_signals_df = self.shuffle_rest_vectors(tr_signals_df)
            clips = tr_signals_df.iloc[:, :N_VECTORS // 2]
            rest = tr_signals_df.iloc[:, N_VECTORS // 2:]

        else:
            clips = tr_signals_df.iloc[:, :N_VECTORS:2]
            rest = tr_signals_df.iloc[:, 1:N_VECTORS:2]

        concat_clips = np.concatenate(clips.values)
        concat_rests = np.concatenate(rest.values)

        concat_clips_z = z_score(concat_clips)
        concat_rests_z = z_score(concat_rests)

        df_concatenated_signals = pd.DataFrame({'concat_clip': concat_clips_z, 'concat_rest': concat_rests_z})
        df_corr = df_concatenated_signals.corr()
        distance = round(df_corr.loc['concat_clip'].at['concat_rest'], 3)

        return distance, df_concatenated_signals

    def average_data_flow(self, roi, **kwargs):
        init_window_task = kwargs.pop('init_window')
        ws_task = kwargs.pop('task_ws')
        ws_rest = kwargs.pop('rest_ws')
        clip_window = kwargs.get('window_range', ('', ''))
        single_movie_activation = kwargs.pop('movie_activation', False)

        _range = f'task_{init_window_task}{clip_window[0]}{clip_window[1]}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr'

        output_dir = config.FMRI_SINGLE_MOVIE_ACTIVATIONS_PATTERN_RESULTS.format(
            range=_range,
            group_amount=kwargs['group_subjects'],
            group_index=kwargs['group_index']
        )

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        save_path = os.path.join(output_dir, f"{roi}.pkl")
        if os.path.isfile(save_path):
            return

        roi_data_task = self.load_group_subjects(roi=roi, mode=Mode.CLIPS, **kwargs)
        roi_data_rest = self.load_group_subjects(roi=roi, mode=Mode.REST, **kwargs)

        _, tr_vectors_df = self.custom_temporal_relational_coding(
            data_task=roi_data_task,
            data_rest=roi_data_rest,
            window_size_rest=ws_rest,
            init_window_task=init_window_task,
            window_size_task=ws_task,
            **kwargs
        )

        if single_movie_activation:
            activation_values = {}
            for i in range(0, 28, 2):
                clip_rest_pair = tr_vectors_df.iloc[:, i:i + 2]
                corr = clip_rest_pair.corr()
                clip_name = corr.columns.tolist()[0].replace('_task', '')
                distance = round(corr.loc[f'{clip_name}_task'].at[f'{clip_name}_rest'], 3)
                activation_values[clip_name] = distance


        else:
            distance, concat_signals = self._correlate_concatenated_signals(tr_vectors_df, **kwargs)
            activation_values = {'activation_pattern': distance, 'concat_signals': concat_signals}

        utils.dict_to_pkl(activation_values, save_path.replace('.pkl', ''))

    def run(self, roi: str, *args, **kwargs):

        self.average_data_flow(roi, **kwargs)

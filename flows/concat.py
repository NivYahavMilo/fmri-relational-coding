"""Concatenated-signal activation patterns (was ConcatFmriTemporalRelationalCoding)."""
import os

import settings
import data_access
import rc_core
from data_normalizer import utils
from enums import Mode


def _average_data_flow(roi, **kwargs):
    init_window_task = kwargs.pop('init_window')
    ws_task = kwargs.pop('task_ws')
    ws_rest = kwargs.pop('rest_ws')
    clip_window = kwargs.get('window_range', ('', ''))
    single_movie_activation = kwargs.pop('movie_activation', False)

    _range = f'task_{init_window_task}{clip_window[0]}{clip_window[1]}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr'
    output_dir = settings.FMRI_SINGLE_MOVIE_ACTIVATIONS_PATTERN_RESULTS.format(
        range=_range, group_amount=kwargs['group_subjects'], group_index=kwargs['group_index'])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = os.path.join(output_dir, f"{roi}.pkl")
    if os.path.isfile(save_path):
        return

    roi_data_task = data_access.load_group_subjects(
        roi=roi, mode=Mode.CLIPS, n_subjects=kwargs['group_subjects'], group_index=kwargs['group_index'])
    roi_data_rest = data_access.load_group_subjects(
        roi=roi, mode=Mode.REST, n_subjects=kwargs['group_subjects'], group_index=kwargs['group_index'])

    _, tr_vectors_df = rc_core.custom_temporal_relational_coding(
        data_task=roi_data_task, data_rest=roi_data_rest,
        window_size_rest=ws_rest, init_window_task=init_window_task, window_size_task=ws_task, **kwargs)

    if single_movie_activation:
        activation_values = {}
        for i in range(0, 28, 2):
            clip_rest_pair = tr_vectors_df.iloc[:, i:i + 2]
            corr = clip_rest_pair.corr()
            clip_name = corr.columns.tolist()[0].replace('_task', '')
            distance = round(corr.loc[f'{clip_name}_task'].at[f'{clip_name}_rest'], 3)
            activation_values[clip_name] = distance
    else:
        distance, concat_signals = rc_core.correlate_concatenated_signals(tr_vectors_df, **kwargs)
        activation_values = {'activation_pattern': distance, 'concat_signals': concat_signals}

    utils.dict_to_pkl(activation_values, save_path.replace('.pkl', ''))


def run(roi, **kwargs):
    _average_data_flow(roi, **kwargs)

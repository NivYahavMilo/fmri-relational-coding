"""Core relational-coding algorithms as plain functions.

These were previously methods on ``RelationalCodingBase`` / ``CustomTemporalRelationalCodingUtils``.
The analysis flows now compose these functions instead of inheriting a base class.
"""
import numpy as np
import pandas as pd

from arithmetic_operations import distances_utils
from arithmetic_operations.correlation_and_standardization import z_score
from arithmetic_operations.decomposition import Decomposition
from arithmetic_operations.matrix_op import MatrixOperations
from arithmetic_operations.signal_processing import SignalProcessing
from data_center.static_data.static_data import StaticData


def drop_metadata_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return `df` without the non-voxel metadata columns (y, timepoint, and Subject if present)."""
    drop_columns = ['y', 'timepoint']
    if 'Subject' in df.columns:
        drop_columns.append('Subject')
    return df.drop(drop_columns, axis=1)


def get_clip_name_by_index(i):
    return StaticData.CLIP_MAPPING.get(str(i))


def rearrange_clip_order(df):
    clip_order = StaticData.CLIPS_ORDER + StaticData.REST_ORDER
    return df[clip_order]


def shuffle_rest_vectors(df):
    rest_clips = StaticData.REST_ORDER.copy()
    np.random.shuffle(rest_clips)
    clip_order = StaticData.CLIPS_ORDER + rest_clips
    return df[clip_order]


def rest_between_tr_generator():
    for i in range(19):
        yield i


def subjects_generator():
    for sub in StaticData.SUBJECTS:
        yield sub


def get_single_tr_vector(data: pd.DataFrame, clip_i: int, timepoint: int = -1):
    if timepoint == -1:
        xdf = data[data['y'] == clip_i]
        timepoint = int(max(xdf['timepoint'].values))

    sequence = data[(data['timepoint'] == timepoint) & (data['y'] == clip_i)]
    sequence = drop_metadata_columns(sequence)
    return sequence.values[0].tolist()


def correlate_current_timepoint(data, **kwargs):
    df = pd.DataFrame.from_dict(data, orient='columns')
    df = rearrange_clip_order(df)

    if kwargs.get('shuffle_rest'):
        df = shuffle_rest_vectors(df)

    if kwargs.get('filtering'):
        df = SignalProcessing.low_pass_filtering(
            df, filter_order=kwargs.get('filter_order'), cut_off=kwargs.get('filter_cut_off'))

    if kwargs.get('decomposition'):
        df = Decomposition.reduce_dimensions(df, n_components=0.1)

    if kwargs.get('movie_distances'):
        df = distances_utils.create_distances_movies_vector(df)

    df_corr = df.corr()
    rest_cor = df_corr.iloc[len(df_corr) // 2:, len(df_corr) // 2:]
    clip_cor = df_corr.iloc[:len(df_corr) // 2, :len(df_corr) // 2]

    flat_corr_rest = MatrixOperations.drop_symmetric_side_of_a_matrix(rest_cor)
    flat_corr_task = MatrixOperations.drop_symmetric_side_of_a_matrix(clip_cor)

    general_corr = pd.DataFrame()
    general_corr['task'] = flat_corr_task
    general_corr['rest'] = flat_corr_rest

    tr_corr = general_corr.corr()
    distance = round(tr_corr.loc['task'].at['rest'], 3)
    return distance, df_corr.fillna(1)


def get_task_window_slides_vectors(data_task, clip_i, init_window, window_size_task, **kwargs):
    clip_ct = data_task[(data_task['y'] == clip_i)]

    if init_window == 'start':
        init_timepoint = clip_ct['timepoint'].min()
        clip_window = range(init_timepoint, window_size_task)

    elif init_window in ('end', 'shuffle'):
        init_timepoint = clip_ct['timepoint'].max()
        clip_window = range(init_timepoint - window_size_task + 1, init_timepoint + 1)

    elif init_window == 'middle':
        init_timepoint = clip_ct['timepoint'].min() + (clip_ct['timepoint'].max() - clip_ct['timepoint'].min()) // 2
        clip_window = range(init_timepoint - window_size_task // 2, init_timepoint + window_size_task // 2)

    elif init_window == 'dynamic':
        s, e = kwargs.pop('window_range')
        clip_window = range(s, e)

    elif init_window == 'moving_window_from_end':
        init_timepoint = clip_ct['timepoint'].max() - kwargs.get('window_moving_size')
        clip_window = range(init_timepoint - window_size_task + 1, init_timepoint + 1)

    else:
        raise ValueError('init_window value wrong')

    clip_ct_window = drop_metadata_columns(clip_ct[clip_ct['timepoint'].isin(clip_window)])
    return np.mean(clip_ct_window.values, axis=0)


def add_tr_from_next_clip(window_indices, **kwargs):
    clip_data = kwargs.pop('clip_data')
    next_clip = kwargs.pop('next_clip')
    if next_clip == 15:
        next_clip = 1
    clip_data = clip_data[clip_data['y'] == next_clip]
    if clip_data.empty:
        return pd.DataFrame()

    start_tr, end_tr = window_indices
    new_end_of_clip = end_tr - kwargs['max_rest_tr']

    if start_tr <= kwargs['max_rest_tr']:
        tr_range = range(0, new_end_of_clip)
    else:
        new_start_of_clip = start_tr - kwargs['max_rest_tr']
        tr_range = range(new_start_of_clip, new_end_of_clip)

    clip_data_window = clip_data[clip_data['timepoint'].isin(tr_range)]
    return drop_metadata_columns(clip_data_window)


def get_rest_window_slides_vectors(data_rest, clip_i, window_size_rest, **kwargs):
    rest_ct = data_rest[data_rest['y'] == clip_i]
    start, end = window_size_rest

    rest_ct_window = drop_metadata_columns(rest_ct[rest_ct['timepoint'].isin(range(start, end))])

    max_timepoint = max(rest_ct['timepoint'])
    if max_timepoint < end:
        kwargs['max_rest_tr'] = max_timepoint
        extra_clip_window = add_tr_from_next_clip(window_indices=window_size_rest, next_clip=clip_i + 1, **kwargs)
        rest_ct_window = pd.concat([rest_ct_window, extra_clip_window])

    return np.mean(rest_ct_window.values, axis=0)


def custom_temporal_relational_coding(*, data_task, data_rest, window_size_rest,
                                      init_window_task, window_size_task, **kwargs):
    custom_temporal_window_vec = {}
    for clip_i in range(1, 15):
        clip_name = get_clip_name_by_index(clip_i)
        task_window_avg = get_task_window_slides_vectors(
            data_task, clip_i, init_window_task, window_size_task, **kwargs)
        rest_window_avg = get_rest_window_slides_vectors(
            data_rest, clip_i, window_size_rest, clip_data=data_task)
        custom_temporal_window_vec[clip_name + '_task'] = task_window_avg
        custom_temporal_window_vec[clip_name + '_rest'] = rest_window_avg

    if kwargs.get('skip_correlation'):
        return None, pd.DataFrame(custom_temporal_window_vec)

    rc_distance, _ = correlate_current_timepoint(data=custom_temporal_window_vec, **kwargs)
    return rc_distance, pd.DataFrame(custom_temporal_window_vec)


def get_avg_rest_matrix(rest_data, clip_index):
    rd_clip = rest_data[rest_data['y'] == clip_index]
    rd_clip = drop_metadata_columns(rd_clip)
    return np.mean(rd_clip.values, axis=0)


def singular_relational_coding(d_task, d_rest):
    singular_corr = {}
    for clip_i in range(1, 15):
        clip_name = get_clip_name_by_index(clip_i)
        task_vector = get_single_tr_vector(data=d_task, clip_i=clip_i)
        rest_avg_vec = get_avg_rest_matrix(rest_data=d_rest, clip_index=clip_i)
        score = np.corrcoef(task_vector, rest_avg_vec)
        singular_corr[clip_name] = score[0, 1]
    return singular_corr


def correlate_concatenated_signals(tr_signals_df, **kwargs):
    n_vectors = 28
    if kwargs.get('shuffle_rest'):
        tr_signals_df = shuffle_rest_vectors(tr_signals_df)
        clips = tr_signals_df.iloc[:, :n_vectors // 2]
        rest = tr_signals_df.iloc[:, n_vectors // 2:]
    else:
        clips = tr_signals_df.iloc[:, :n_vectors:2]
        rest = tr_signals_df.iloc[:, 1:n_vectors:2]

    concat_clips = np.concatenate(clips.values)
    concat_rests = np.concatenate(rest.values)

    concat_clips_z = z_score(concat_clips, axis=0)
    concat_rests_z = z_score(concat_rests, axis=0)

    df_concatenated_signals = pd.DataFrame({'concat_clip': concat_clips_z, 'concat_rest': concat_rests_z})
    df_corr = df_concatenated_signals.corr()
    distance = round(df_corr.loc['concat_clip'].at['concat_rest'], 3)
    return distance, df_concatenated_signals

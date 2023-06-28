import os
import random
from abc import abstractmethod

import numpy as np
import pandas as pd

import config
from arithmetic_operations.matrix_op import MatrixOperations
from arithmetic_operations.signal_processing import SignalProcessing
from arithmetic_operations.decomposition import Decomposition
from arithmetic_operations import distances_utils
from data_center.static_data.static_data import StaticData
from enums import Mode


class RelationalCodingBase:

    def correlate_current_timepoint(self, data, **kwargs):
        df = pd.DataFrame.from_dict(data, orient='columns')
        df = self.rearrange_clip_order(df)

        # shuffle for results control
        if kwargs.get('shuffle_rest'):
            df = self.shuffle_rest_vectors(df)

        if kwargs.get('filtering'):
            filter_order = kwargs.get('filter_order')
            cut_off = kwargs.get('filter_cut_off')
            df = SignalProcessing.low_pass_filtering(df, filter_order=filter_order, cut_off=cut_off)

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

    @staticmethod
    def rearrange_clip_order(df):
        clip_order = StaticData.CLIPS_ORDER + StaticData.REST_ORDER
        df = df[clip_order]
        return df

    @staticmethod
    def shuffle_rest_vectors(df):
        rest_clips = StaticData.REST_ORDER.copy()
        np.random.shuffle(rest_clips)
        clip_order = StaticData.CLIPS_ORDER + rest_clips
        df = df[clip_order]
        return df

    @staticmethod
    def get_clip_name_by_index(i):
        return StaticData.CLIP_MAPPING.get(str(i))

    @staticmethod
    def get_single_tr_vector(data: pd.DataFrame, clip_i: int, timepoint: int = -1):
        drop_columns = []

        if timepoint == -1:
            xdf = data[data['y'] == clip_i]
            timepoint = int(max(xdf['timepoint'].values))

        sequence = data[(data['timepoint'] == timepoint) &
                        (data['y'] == clip_i)]

        if 'Subject' in sequence.columns:
            drop_columns.append('Subject')
        drop_columns.extend(['y', 'timepoint'])

        sequence = sequence.drop(drop_columns, axis=1)

        return sequence.values[0].tolist()

    @staticmethod
    def rest_between_tr_generator():
        for i in range(19):
            yield i

    @staticmethod
    def yield_subject_generator():
        for sub in StaticData.SUBJECTS:
            yield sub

    def load_roi_data(self, roi_name: str, subject: str, mode: Mode):
        self._check_roi_validity(roi_name)
        # if pass validity checks
        data_path = config.SUBNET_DATA_DF.format(mode=mode.value)
        roi_data_p = os.path.join(data_path, subject, f"{roi_name}.pkl")
        roi_data_df = pd.read_pickle(roi_data_p)
        return roi_data_df

    def load_avg_data(self, roi_name: str, mode: Mode, group: str = ''):
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

    @abstractmethod
    def run(self, roi: str, *args, **kwargs):
        """
        run relational coding flow.
        """
        pass

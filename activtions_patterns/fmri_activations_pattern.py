import os

import pandas as pd

import config
from activtions_patterns.base_activations_pattern import BaseActivationPattern
import data_normalizer.utils as utils
from enums import Mode


class FmriActivationPattern(BaseActivationPattern):


    def extract_correlation_values(self, df):
        corr_values = {}
        for i in range(1,15):
            clip_name = self.get_clip_name_by_index(i)
            corr_value = df.loc[f'{clip_name}_task'].at[f'{clip_name}_rest']
            corr_values[clip_name] = corr_value

        return corr_values


    def get_activation_pattern(self, d_task, d_rest):
        tr_corr = {}
        for tr in self.rest_between_tr_generator():
            timepoint_clip_matrix = self.get_clip_vectors(
                rest_data=d_rest,
                task_data=d_task,
                timepoint=tr)

            df_corr = self.correlate_current_timepoint(data=timepoint_clip_matrix)
            correlation_dict = self.extract_correlation_values(df_corr)
            tr_corr[tr] = correlation_dict
        return tr_corr

    def get_clip_vectors(self, rest_data, task_data, timepoint):
        tr_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)

            task_vector = self.get_single_tr_vector(data=task_data, clip_i=clip_i)
            tr_vec[clip_name + '_task'] = task_vector

            rest_vector = self.get_single_tr_vector(data=rest_data, clip_i=clip_i, timepoint=timepoint)
            tr_vec[clip_name + '_rest'] = rest_vector

        return tr_vec

    def correlate_current_timepoint(self, data):
        df = pd.DataFrame.from_dict(data, orient='columns')
        df = self.rearrange_clip_order(df)
        df_corr = df.corr()

        return df_corr

    def avg_data_flow(self, roi, res_path, group):
        roi_avg_task = self.load_avg_data(roi_name=roi, mode=Mode.CLIPS, group=group)
        roi_avg_rest = self.load_avg_data(roi_name=roi, mode=Mode.REST, group=group)
        tr_corr = self.get_activation_pattern(d_rest=roi_avg_rest, d_task=roi_avg_task)
        utils.dict_to_pkl(tr_corr, res_path.replace('.pkl', ''))
        print(f'Saved roi {roi}')

    def run(self, roi: str, group: str):
        save_path = os.path.join(config.FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG.format(group=group.lower()), f"{roi}.pkl")
        if os.path.isfile(save_path):
            return
        self.avg_data_flow(roi, save_path, group)

import os.path

import pandas as pd

import config
import data_normalizer.utils as utils
from arithmetic_operations.matrix_op import MatrixOperations
from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase


class FmriRelationalCoding(RelationalCodingBase):

    def correlate_current_timepoint(self, data):
        df = pd.DataFrame.from_dict(data, orient='columns')
        df = self.rearrange_clip_order(df)
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

    def get_clip_vectors(self, rest_data, task_data, timepoint):
        tr_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)

            task_vector = self.get_single_tr_vector(data=task_data, clip_i=clip_i)
            tr_vec[clip_name + '_task'] = task_vector

            rest_vector = self.get_single_tr_vector(data=rest_data, clip_i=clip_i, timepoint=timepoint)
            tr_vec[clip_name + '_rest'] = rest_vector

        return tr_vec

    def relation_distance(self, d_rest, d_task):
        sub_rc_dis = []
        sub_rc_corr = []
        for tr in self.rest_between_tr_generator():
            timepoint_clip_matrix = self.get_clip_vectors(
                rest_data=d_rest,
                task_data=d_task,
                timepoint=tr)

            rc_distance, corr_df = self.correlate_current_timepoint(data=timepoint_clip_matrix)
            sub_rc_dis.append(rc_distance)
            sub_rc_corr.append(corr_df)
        return sub_rc_dis, sub_rc_corr

    def avg_data_flow(self, roi, res_path, group):
        data = {}
        roi_avg_task = self.load_avg_data(roi_name=roi, mode=Mode.CLIPS, group=group)
        roi_avg_rest = self.load_avg_data(roi_name=roi, mode=Mode.REST, group=group)
        sub_rc_dis, df_corr = self.relation_distance(d_rest=roi_avg_rest, d_task=roi_avg_task)
        # store results in subject id key
        data['avg'] = sub_rc_dis
        data['avg correlation'] = df_corr
        # save subject result
        utils.dict_to_pkl(data, res_path.replace('.pkl', ''))
        print(f'Saved roi {roi}')

    def subject_flow(self, roi, res_path):
        data = {}
        for sub_id in self.yield_subject_generator():
            roi_sub_data_task = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)
            sub_rc_dis, _ = self.relation_distance(d_rest=roi_sub_data_rest, d_task=roi_sub_data_task)
            # store results in subject id key
            data[sub_id] = sub_rc_dis
        # save subject result
        utils.dict_to_pkl(data, res_path.replace('.pkl', ''))
        print(f'Saved roi {roi}')

    def run(self, roi, avg_data: bool = False, group: str = ''):
        if avg_data:
            save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS_AVG.format(group=group.lower()), f"{roi}.pkl")
            if os.path.isfile(save_path):
                return
            self.avg_data_flow(roi, save_path, group)
        else:
            save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS, f"{roi}.pkl")
            if os.path.isfile(save_path):
                return
            self.subject_flow(roi, save_path)

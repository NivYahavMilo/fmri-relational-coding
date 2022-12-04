import os.path

import pandas as pd

import config
from arithmetic_operations.matrix_op import MatrixOperations
from data_normalizer.utils import _dict_to_pkl
from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase


class FmriRelationalCoding(RelationalCodingBase):

    def __init__(self):
        self.relation_coding = {}

    def correlate_current_timepoint(self, data, timepoint):
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
        self.relation_coding[timepoint] = distance

    def get_clip_vectors(self, rest_data, task_data, timepoint):
        tr_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)

            task_vector = self.get_single_tr_vector(data=task_data, clip_i=clip_i)
            tr_vec[clip_name + '_task'] = task_vector

            rest_vector = self.get_single_tr_vector(data=rest_data, clip_i=clip_i, timepoint=timepoint)
            tr_vec[clip_name + '_rest'] = rest_vector

        return tr_vec

    def run(self, roi):

        data = {}
        for sub_id in self.yield_subject_generator():
            roi_sub_data_task = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)

            for tr in self.rest_between_tr_generator():
                timepoint_clip_matrix = self.get_clip_vectors(
                    rest_data=roi_sub_data_rest,
                    task_data=roi_sub_data_task,
                    timepoint=tr)

                self.correlate_current_timepoint(data=timepoint_clip_matrix, timepoint=tr)

            data[sub_id] = self.relation_coding
            self.relation_coding.clear()

        save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS, roi)
        _dict_to_pkl(data, save_path)
        print(f'Saved roi {roi}')

import os

import numpy as np

import config
from data_normalizer import utils
from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase


class SingularRelationalCoding(RelationalCodingBase):

    @staticmethod
    def _get_avg_rest_matrix(rest_data, clip_index):
        rd_clip = rest_data[rest_data['y'] == clip_index]
        rd_clip = rd_clip.drop(['y', 'Subject', 'timepoint'], axis=1)
        return np.mean(rd_clip.values, axis=0)

    def singular_relational_coding(self, d_task, d_rest):
        singular_corr = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)

            task_vector = self.get_single_tr_vector(data=d_task, clip_i=clip_i)
            rest_avg_vec = self._get_avg_rest_matrix(rest_data=d_rest, clip_index=clip_i)
            score = np.corrcoef(task_vector, rest_avg_vec)
            singular_corr[clip_name] = score[0, 1]

        return singular_corr

    def run(self, roi: str, *args, **kwargs):
        save_path = os.path.join(config.FMRI_RELATION_CODING_RESULTS, f"{roi}.pkl")
        if os.path.isfile(save_path):
            return
        data = {}
        for sub_id in self.yield_subject_generator():
            roi_sub_data_task = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)
            sub_rc_dis = self.singular_relational_coding(d_rest=roi_sub_data_rest, d_task=roi_sub_data_task)
            # store results in subject id key
            data[sub_id] = sub_rc_dis
        # save subject result
        utils.dict_to_pkl(data, save_path.replace('.pkl', ''))
        print(f'Saved roi {roi}')

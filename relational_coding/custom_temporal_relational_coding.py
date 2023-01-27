import os

import numpy as np

import config
from arithmetic_operations.correlation_and_standartization import z_score
from data_normalizer import utils
from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase


class CustomTemporalRelationalCoding(RelationalCodingBase):

    @staticmethod
    def __get_rest_window_slides_vectors(data_rest, clip_i, window_size_rest):
        drop_columns = []

        rest_ct = data_rest[data_rest['y'] == clip_i]
        start, end = window_size_rest

        if 'Subject' in rest_ct.columns:
            drop_columns.append('Subject')
        drop_columns.extend(['y', 'timepoint'])

        rest_ct_window = rest_ct[rest_ct['timepoint'].isin(range(start, end))].drop(drop_columns, axis=1)
        rest_window_avg = np.mean(rest_ct_window.values, axis=0)
        rest_window_avg_z = z_score(rest_window_avg)

        return rest_window_avg_z

    @staticmethod
    def __get_task_window_slides_vectors(data_task, clip_i, init_window, window_size_task):
        drop_columns = []

        clip_ct = data_task[(data_task['y'] == clip_i)]

        if init_window == 'start':
            init_timepoint = clip_ct['timepoint'].min()
            clip_window = range(init_timepoint, window_size_task)

        elif init_window == 'end':
            init_timepoint = clip_ct['timepoint'].max()
            clip_window = range(init_timepoint - window_size_task, init_timepoint)

        elif init_window == 'middle':
            init_timepoint = clip_ct['timepoint'].min() + (clip_ct['timepoint'].max() - clip_ct['timepoint'].min()) // 2
            clip_window = range(init_timepoint - window_size_task // 2, init_timepoint + window_size_task // 2)

        else:
            raise ValueError('init_window value wrong')

        if 'Subject' in clip_ct.columns:
            drop_columns.append('Subject')
        drop_columns.extend(['y', 'timepoint'])

        clip_ct_window = clip_ct[clip_ct['timepoint'].isin(clip_window)].drop(drop_columns, axis=1)
        task_window_avg = np.mean(clip_ct_window.values, axis=0)
        task_window_avg_z = z_score(task_window_avg)

        return task_window_avg_z

    def __custom_temporal_relational_coding(
            self,
            *,
            data_task,
            data_rest,
            window_size_rest,
            init_window_task,
            window_size_task,
            shuffle
    ):

        custom_temporal_window_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)
            task_window_avg = self.__get_task_window_slides_vectors(data_task, clip_i, init_window_task,
                                                                    window_size_task)
            rest_window_avg = self.__get_rest_window_slides_vectors(data_rest, clip_i, window_size_rest)
            custom_temporal_window_vec[clip_name + '_task'] = task_window_avg
            custom_temporal_window_vec[clip_name + '_rest'] = rest_window_avg

        rc_distance, _ = self.correlate_current_timepoint(data=custom_temporal_window_vec, shuffle_rest=shuffle)
        return rc_distance

    def __subject_flow(self, roi, init_window_task, ws_task, ws_rest, shuffle):
        output_dir = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS.format(
            range=f'task_{init_window_task}_{ws_task}_tr_rest{ws_rest[0]}-{ws_rest[1]}_tr')

        save_path = os.path.join(output_dir, f"{roi}.pkl")

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if os.path.isfile(save_path):
            return
        data = {}
        for sub_id in self.yield_subject_generator():
            roi_sub_data_task = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)

            rc_distance = self.__custom_temporal_relational_coding(
                data_task=roi_sub_data_task,
                data_rest=roi_sub_data_rest,
                window_size_rest=ws_rest,
                init_window_task=init_window_task,
                window_size_task=ws_task,
                shuffle=shuffle)

            data[sub_id] = rc_distance

        utils.dict_to_pkl(data, save_path.replace('.pkl', ''))

    def __avg_flow(self, roi, init_window_task, ws_task, ws_rest, shuffle):

        output_dir = config.FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG.format(
            range=f'task_{init_window_task}_{ws_task}_tr_rest_{ws_rest[0]}-{ws_rest[1]}_tr')

        save_path = os.path.join(output_dir, f"{roi}.pkl")

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if os.path.isfile(save_path):
            return

        data = {}
        roi_data_task = self.load_avg_data(roi_name=roi, mode=Mode.CLIPS)
        roi_data_rest = self.load_avg_data(roi_name=roi, mode=Mode.REST)

        rc_distance = self.__custom_temporal_relational_coding(
            data_task=roi_data_task,
            data_rest=roi_data_rest,
            window_size_rest=ws_rest,
            init_window_task=init_window_task,
            window_size_task=ws_task,
            shuffle=shuffle)

        data['avg'] = rc_distance

        utils.dict_to_pkl(data, save_path.replace('.pkl', ''))
        print(f'saved {roi}')

    def run(self, roi: str, *args, **kwargs):
        init_window_task = kwargs['init_window_task']
        ws_task = kwargs['task_window_size']
        ws_rest = kwargs['rest_window_size']
        avg_data = kwargs['average_data']
        shuffle = kwargs.get('shuffle_rest', False)
        if avg_data:
            self.__avg_flow(
                roi=roi,
                init_window_task=init_window_task,
                ws_task=ws_task,
                ws_rest=ws_rest,
                shuffle=shuffle,
            )
            return

        self.__subject_flow(
            roi=roi,
            init_window_task=init_window_task,
            ws_task=ws_task,
            ws_rest=ws_rest,
            shuffle=shuffle,
        )

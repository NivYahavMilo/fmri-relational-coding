import numpy as np
import pandas as pd

from arithmetic_operations.correlation_and_standartization import z_score
from relational_coding.relational_coding_base import RelationalCodingBase

class CustomTemporalRelationalCodingUtils(RelationalCodingBase):

    def custom_temporal_relational_coding(
            self,
            *,
            data_task,
            data_rest,
            window_size_rest,
            init_window_task,
            window_size_task,
            **kwargs
    ):

        custom_temporal_window_vec = {}
        for clip_i in range(1, 15):
            clip_name = self.get_clip_name_by_index(clip_i)
            task_window_avg = self.get_task_window_slides_vectors(data_task, clip_i, init_window_task, window_size_task)
            rest_window_avg = self.get_rest_window_slides_vectors(data_rest, clip_i, window_size_rest)
            custom_temporal_window_vec[clip_name + '_task'] = task_window_avg
            custom_temporal_window_vec[clip_name + '_rest'] = rest_window_avg

        rc_distance, _ = self.correlate_current_timepoint(data=custom_temporal_window_vec, **kwargs)

        custom_temporal_window_vec = pd.DataFrame(custom_temporal_window_vec)
        return rc_distance, custom_temporal_window_vec

    @staticmethod
    def get_rest_window_slides_vectors(data_rest, clip_i, window_size_rest):
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
    def get_task_window_slides_vectors(data_task, clip_i, init_window, window_size_task):
        drop_columns = []

        clip_ct = data_task[(data_task['y'] == clip_i)]

        if init_window == 'start':
            init_timepoint = clip_ct['timepoint'].min()
            clip_window = range(init_timepoint, window_size_task)

        elif init_window == 'end':
            init_timepoint = clip_ct['timepoint'].max()
            clip_window = range(init_timepoint - window_size_task+1, init_timepoint+1)

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

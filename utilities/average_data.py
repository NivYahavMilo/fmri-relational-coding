import os

import pandas as pd

import config
from arithmetic_operations.matrix_op import MatrixOperations
from data_center.static_data.static_data import StaticData
from data_normalizer import utils
from enums import Mode

StaticData.inhabit_class_members()


def _load(sub, roi, mode):
    data_path = config.SUBNET_DATA_DF.format(mode=mode.value)
    roi_data_p = os.path.join(data_path, sub, f'{roi}.pkl')
    roi_data_df = pd.read_pickle(roi_data_p)
    return roi_data_df


def get_subjects_average_roi_matrix():
    mid_i = len(StaticData.SUBJECTS) // 2
    group1 = StaticData.SUBJECTS[:mid_i]
    group2 = StaticData.SUBJECTS[mid_i:]

    for roi in StaticData.ROI_NAMES:
        save_path_rest = os.path.join(config.SUBNET_DATA_AVG.format(mode=Mode.REST.value,
                                                                    group='_GROUP2'), f'{roi}')
        save_path_task = os.path.join(config.SUBNET_DATA_AVG.format(mode=Mode.CLIPS.value,
                                                                    group='_GROUP2'), f'{roi}')
        task = []
        rest = []
        drop = ['timepoint', 'Subject', 'y']
        for sub_id in group2:
            roi_sub_data_task = _load(roi=roi, sub=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = _load(roi=roi, sub=sub_id, mode=Mode.REST)
            roi_sub_data_task_d = roi_sub_data_task.drop(drop, axis=1)
            roi_sub_data_rest_d = roi_sub_data_rest.drop(drop, axis=1)
            task.append(roi_sub_data_task_d.values)
            rest.append(roi_sub_data_rest_d.values)

        rest_avg = pd.DataFrame(MatrixOperations.get_avg_matrix(rest))
        task_avg = pd.DataFrame(MatrixOperations.get_avg_matrix(task))

        rest_avg['timepoint'] = roi_sub_data_rest['timepoint']
        rest_avg['y'] = roi_sub_data_rest['y']
        task_avg['timepoint'] = roi_sub_data_task['timepoint']
        task_avg['y'] = roi_sub_data_task['y']

        utils.dict_to_pkl(rest_avg, save_path_rest)
        utils.dict_to_pkl(task_avg, save_path_task)
        print(f'Saved roi {roi}')


def get_average_data_leave_one_out():
    for roi in StaticData.ROI_NAMES:
        for subject in StaticData.SUBJECTS:
            remaining_subjects = StaticData.SUBJECTS.copy()
            remaining_subjects.remove(subject)
            rest_subject_data = []
            for sub in remaining_subjects:
                df = _load(roi=roi, sub=sub, mode=Mode.REST)
                df_values = df.drop(['timepoint', 'Subject', 'y'], axis=1)
                rest_subject_data.append(df_values.values)



            save_path = os.path.join(config.SUBJECTS_AVG_DATA_LEAVE_ONE_OUT, subject)
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            roi_path = os.path.join(save_path, f'{roi}.pkl')
            if os.path.isfile(roi_path):
                continue

            mean_data = pd.DataFrame(MatrixOperations.get_avg_matrix(rest_subject_data))
            mean_data['timepoint'] = df['timepoint']
            mean_data['y'] = df['y']
            mean_data.to_pickle(roi_path)

            pass




if __name__ == '__main__':
    # get_subjects_average_roi_matrix()
    get_average_data_leave_one_out()
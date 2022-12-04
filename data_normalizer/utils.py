import os
import pickle

import numpy as np
import pandas as pd

import config


def info(s: str):
    print('-' * 10)
    print(s)
    print('-' * 10)


def get_parcel(roi, net=7):
    """
    load voxel and networks mapping according to parcel file
    return:
    parcel: grayordinate -> ROI map
    nw_info: subnetwork tags for each ROI
    """
    parcel_path = os.path.join(config.DATA_DRIVE_E, 'cifti',
                               'Schaefer2018_%dParcels_%dNetworks_order.csv' % (roi, net))

    df = pd.read_csv(parcel_path)
    parcel = np.array(df['ROI'])

    info_path = parcel_path.replace('.csv', '_info_condensed.csv')
    df = pd.read_csv(info_path)
    nw_info = np.array(df['network'])

    return parcel, nw_info


def get_clip_labels(timing_file, k_runs: int = 4):
    """
    assign all clips within runs a label
    use 0 for testretest
    """

    clips = []
    for run in range(k_runs):
        run_name = 'MOVIE%d' % (run + 1)  # MOVIEx_7T_yz
        timing_df = timing_file[timing_file['run'].str.contains(run_name)]
        timing_df = timing_df.reset_index(drop=True)

        for jj, row in timing_df.iterrows():
            clips.append(row['clip_name'])

    clip_y = {}
    jj = 1
    for clip in clips:
        if 'testretest' in clip:
            clip_y[clip] = 0
        else:
            clip_y[clip] = jj
            jj += 1

    return clip_y


def dict_to_pkl(data: dict, file_name: str):
    with open(f'{file_name}.pkl', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pkl(file_name: str):
    file = open(file_name, 'rb')
    object_file = pickle.load(file)
    return object_file

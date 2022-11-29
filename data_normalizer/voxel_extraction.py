import os
import pickle

import numpy as np
import pandas as pd

import config
from data_normalizer.utils import _get_clip_labels, _info
from enums import Mode


def _clip_class_df(data, subject, clip_y, k_runs, timing_file):
    """
    save each timepoint as feature vector
    append class label based on clip
    return:
    """
    table = []
    idx = np.ones(config.GRAYORIDNATES).astype(bool)
    for k_run in range(k_runs):

        run_name = 'MOVIE%d' % (k_run + 1)  # MOVIEx_7T_yz
        # timing file for run
        timing_df = timing_file[
            timing_file['run'].str.contains(run_name)]
        timing_df = timing_df.reset_index(drop=True)

        # get subject data (time x grayordinate x run)
        roi_ts = data[subject][:, idx, k_run]

        for jj, clip in timing_df.iterrows():

            start = int(np.floor(clip['start_tr']))
            stop = int(np.ceil(clip['stop_tr']))
            clip_length = stop - start

            # assign label to clip
            y = clip_y[clip['clip_name']]

            for t in range(clip_length):
                act = roi_ts[t + start, :]
                t_data = {}
                t_data['Subject'] = subject
                t_data['timepoint'] = t
                for feat in range(roi_ts.shape[1]):
                    t_data['feat_%d' % (feat)] = act[feat]
                t_data['y'] = y
                table.append(t_data)
    del idx, roi_ts, t_data
    return table


def run(mode: Mode):
    timing_file = pd.read_csv(os.path.join(config.TIMING_FILES, f'{mode.value}_TIMING_FILE.csv'))
    clip_y = _get_clip_labels(timing_file)

    subjects_dir = config.VOXEL_DATA

    for sub in os.listdir(subjects_dir):
        sub_id = sub.replace('.pkl', '')[-6:]

        load_path = (os.path.join(config.VOXEL_DATA,
                                  fr'data_MOVIE_runs_voxel_{config.GRAYORIDNATES}_ts_subject_{sub_id}.pkl'))

        output_path = os.path.join(config.VOXEL_DATA_DF.format(mode=mode.value),
                                   f"4_RUNS_VOXEL_LEVEL_SUBJECT_{sub_id}.pkl")

        if not os.path.isfile(output_path):
            with open(load_path, 'rb') as f:
                data = pickle.load(f)

            sub_data = _clip_class_df(data=data, subject=sub_id, clip_y=clip_y, k_runs=4,
                                      timing_file=timing_file)

            df = pd.DataFrame(sub_data)
            df['Subject'] = df['Subject'].astype(int)

            df.to_pickle(os.path.join(config.VOXEL_DATA_DF.format(mode=mode.value),
                                      f"4_RUNS_VOXEL_LEVEL_SUBJECT_{sub_id}.pkl"))
            del df, sub_data, data
            _info(sub_id)


if __name__ == '__main__':
    extraction_mode = Mode.CLIPS
    run(mode=extraction_mode)

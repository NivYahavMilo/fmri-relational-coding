import os

import numpy as np
import pandas as pd

import config
import data_normalizer.utils as utils
from enums import Mode


class VoxelExtraction:

    @staticmethod
    def _clip_class_df(data, subject, clip_y, k_runs, timing_file, resting_state: bool):
        """
        save each timepoint as feature vector
        append class label based on clip
        return:
        """
        table = []
        idx = np.ones(config.K_GRAYORIDNATES).astype(bool)
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

                if resting_state and stop >= 900:
                    stop = 899

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

    @classmethod
    def run(cls, mode: Mode, **kwargs):
        scan_mode = kwargs['scanning_mode'].name
        raw_data_loading_path = kwargs['raw_data_path'].format(scan_mode=scan_mode)
        save_dir_path = kwargs['save_path']
        save_dir_path = save_dir_path.format(mode=mode.value)
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)

        timing_file = pd.read_csv(os.path.join(config.TIMING_FILES, f'{mode.value}_TIMING_FILE.csv'))
        clip_y = utils.get_clip_labels(timing_file)

        for sub in os.listdir(raw_data_loading_path):
            sub_id = sub.replace('.pkl', '')[-6:]

            load_path = os.path.join(raw_data_loading_path,
                                     fr'data_4_runs_voxel_{config.K_GRAYORIDNATES}_ts_subject_{sub_id}.pkl')

            output_path = os.path.join(save_dir_path, f"4_RUNS_VOXEL_LEVEL_SUBJECT_{sub_id}.pkl")

            if not os.path.isfile(output_path):
                data = pd.read_pickle(load_path)

                sub_data = cls._clip_class_df(data=data, subject=sub_id, clip_y=clip_y, k_runs=4,
                                              timing_file=timing_file,
                                              resting_state=True if scan_mode == "REST" else False)

                df = pd.DataFrame(sub_data)
                df['Subject'] = df['Subject'].astype(int)

                df.to_pickle(output_path)
                del df, sub_data, data
                utils.info(sub_id)

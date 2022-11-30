"""
collect participants' runs into data cell
1. extract roi timeseries (ts) from grayordinate ts
2. zscore (normalize) each time series
3. save subject tag
"""
import numpy as np
import nibabel as nib
import os
from glob import glob
import pickle

import config
from enums import Mode
from utils import _info, _get_parcel

class ParcelData:

    @staticmethod
    def _zscore_ts(ts):
        '''
        zscore each ROIs time series
        ts: (time x roi)
        '''
        ts = ts.T
        z_ts = []
        for ii in range(ts.shape[0]):
            t = ts[ii, :]
            z_ts.append((t - np.mean(t)) / np.std(t))

        z_ts = np.array(z_ts)
        z_ts = z_ts.T

        return z_ts

    @classmethod
    def _get_roi_ts(cls, path, parcel):
        '''
        path: path to cifti time series
        parcel: grayordinate -> roi map
            labels range {1, 2, ... , roi}

        return
        roi_ts: time x roi
        '''
        # load cifti, (time x grayordinate)
        ts = nib.load(path).get_fdata()
        # truncate ts to only cortex (rest are subcortical)
        ts = ts[:, :parcel.shape[0]]

        # zscore ts
        z_ts = cls._zscore_ts(ts)  # time x grayordinate
        t = z_ts.shape[0]

        roi_ts = np.zeros((t, config.K_GRAYORIDNATES))
        for ii in range(config.K_GRAYORIDNATES):
            roi_ts[:, ii] = z_ts[:, ii]

        return roi_ts

    @classmethod
    def run(cls, *args, **kwargs):

        mode: Mode = args[0]
        roi = kwargs['k_roi']
        net = kwargs['k_net']

        # load parcellation file
        parcel, nw_info = _get_parcel(roi, net)

        # use glob to get all files with `ext`
        ext = '*MSMAll_hp2000_clean.dtseries.nii'
        files = [y for x in os.walk(config.RAW_DATA.format(mode=mode.value))
                 for y in glob(os.path.join(x[0], ext))]

        # get list of participants
        # ID <=> individual
        participants = set()
        for file in files:
            ID = file.split('\\MNINonLinear')[0][-6:]
            participants.add(ID)
        participants = np.sort(list(participants))
        _info('Number of participants = %d' % len(participants))


        for ii, ID in enumerate(participants):
            ID_files = [file for file in files if ID in file]
            ID_files = np.sort(ID_files)
            data = {}
            # if individual has all 4 runs
            if len(ID_files) == 4:
                _info('%s: %d/%d' % (ID, (ii + 1), len(participants)))
                ID_ts, t = [], []
                for path in ID_files:
                    roi_ts = cls._get_roi_ts(path, parcel)
                    ID_ts.append(roi_ts)
                    t.append(roi_ts.shape[0])
                k_time = np.max(t)

                '''
                ID_ts have different temporal length
                pad zeros
                (time x roi x number of runs)
                '''
                save_ts = np.zeros((k_time, config.K_GRAYORIDNATES, 4))
                for run in range(4):
                    run_ts = ID_ts[run]
                    t = run_ts.shape[0]
                    save_ts[:t, :, run] = run_ts

                data[ID] = save_ts
                SAVE_DIR = config.VOXEL_DATA
                if not os.path.exists(SAVE_DIR):
                    os.makedirs(SAVE_DIR)

                save_path = os.path.join(SAVE_DIR,
                             'data_MOVIE_runs_voxel_%d_ts_subject_%s.pkl' % (config.K_GRAYORIDNATES, ID))
                with open(save_path, 'wb') as f:
                    pickle.dump(data, f)
                del data, save_ts

            else:
                _info('%s not processed' % ID)


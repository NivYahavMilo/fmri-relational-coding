import glob
import os

import numpy as np
import pandas as pd

from data_normalizer import utils
from enums import Network


class MapRoiToNetwork:
    networks_indices = {
        Network.Visual: (range(0, 24), range(150, 173)),
        Network.Limbic: (range(85, 95), range(237, 247)),
        Network.Somatomotor: (range(24, 53), range(173, 201)),
        Network.DorsalAttention: (range(53, 69), range(201, 219)),
        Network.VentralAttention: (range(69, 85), range(219, 237)),
        Network.Default: (range(112, 150), range(270, 300)),
        Network.Frontoparietal: (range(95, 112), range(247, 270)),
    }

    networks_data = {}

    @classmethod
    def slice_network_roi(cls, subject, net: Network, parcel, nw_info):

        subject_data = pd.read_pickle(subject)
        mean_subject_data = cls.mean_voxels_to_roi(subject_data, parcel, nw_info)
        ranges = cls.networks_indices[net]
        range1, range2 = ranges
        mean_subject_data_copy = mean_subject_data.copy()
        mean_subject_data = mean_subject_data.copy().drop(['timepoint', 'Subject', 'y'], axis=1).transpose()
        mean_net_subject = np.concatenate((
            mean_subject_data[mean_subject_data.index.isin((range1))],
            mean_subject_data[mean_subject_data.index.isin((range2))]),
            axis=0
        )

        mean_net_subject = pd.DataFrame(mean_net_subject).transpose()
        mean_net_subject[['timepoint', 'y', 'Subject']] = mean_subject_data_copy[['timepoint', 'y', 'Subject']]
        return mean_net_subject

    @classmethod
    def mean_voxels_to_roi(cls, voxel_data, roi_mapping, network_mapping):
        roi = 300
        roi_ts = np.zeros((voxel_data.shape[0], roi))
        voxel_data_array = voxel_data.copy().drop(['timepoint', 'Subject', 'y'], axis=1).values
        for ii in range(roi):
            roi_ts[:, ii] = np.mean(
                voxel_data_array[:, roi_mapping == (ii + 1)], axis=1)

        # ***reorder based on nw info
        roi_ts = roi_ts[:, np.argsort(network_mapping)]
        roi_ts_df = pd.DataFrame(roi_ts)
        roi_ts_df[['timepoint', 'y', 'Subject']] = voxel_data[['timepoint', 'y', 'Subject']]

        return roi_ts_df

    @classmethod
    def flow(cls, *args, **kwargs):
        parcel, nw_info = utils.get_parcel(roi=300, net=7)
        mode = args[0]
        subjects = glob.glob(kwargs['load_path'].format(mode=mode.value) + '/*')
        for sub in subjects:
            sub_id = sub.split('.pkl')[0][-6:]
            for network in Network:
                save_path = os.path.join(kwargs['save_path'].format(mode=mode.value), network.name)
                subject_file_path = save_path + f'/{sub_id}.pkl'
                if os.path.isfile(save_path):
                    continue
                if not network == Network.WB and not os.path.isfile(subject_file_path):
                    data = cls.slice_network_roi(subject=sub, net=network, parcel=parcel, nw_info=nw_info)

                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    data.to_pickle(subject_file_path)
                    print(f'subject: {sub_id}', f'network {network.name}')

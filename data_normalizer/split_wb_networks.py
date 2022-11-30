import os
import pickle

import numpy as np

import config
from enums import Network


class Roi2Networks:
    networks_indices = {
        Network.Visual: (range(0, 24), range(150, 173)),
        Network.Limbic: (range(85, 95), range(237, 247)),
        Network.Somatomotor: (range(24, 53), range(173, 201)),
        Network.DorsalAttention: (range(53, 69), range(201, 219)),
        Network.VentralAttention: (range(69, 85), range(219, 237)),
        Network.Default: (range(112, 150), range(270, 300)),
        Network.Frontoparietal: (range(95, 112), range(247, 270)),
    }

    @classmethod
    def slice_network_roi(cls, data, net: Network):
        pkl_data = {}
        ranges = cls.networks_indices[net]
        range1, range2 = ranges
        pkl_data[net.name] = np.concatenate((
            data[net.name][:, range1.start:range1.stop, :],
            data[net.name][:, range2.start:range2.stop, :]),
            axis=1)

        data_path = os.path.join(config.DATA_CENTER)
        with open(data_path, 'wb') as f:
            pickle.dump(pkl_data, f)

    @staticmethod
    def load_raw_data():
        #todo: change path to E drive
        data_path = os.path.join(config.DATA_CENTER, 'raw_data')
        file_name = os.listdir(data_path)[0]
        with open(file_name, 'r') as f:
            raw_data = pickle.load(f)

        return raw_data

    @classmethod
    def flow(cls):
        fmri_data = cls.load_raw_data()
        for network in Network:
            if not network == Network.WB:
                cls.slice_network_roi(data=fmri_data, net=network)

# todo: check this code
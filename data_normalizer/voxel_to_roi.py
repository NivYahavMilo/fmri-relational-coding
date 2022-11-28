import glob
from typing import Optional

import pandas as pd

import config
from data_normalizer.utils import _load_pkl


class Voxel2Roi:
    def __init__(self, roi: int, networks: int):
        self.mapping: Optional[pd.DataFrame] = self._load_voxel_mapping_file(roi, networks)

    @staticmethod
    def _load_voxel_mapping_file(roi: int, nw: int):
        parcel_type = f'Schaefer2018_{roi}Parcels_{nw}Networks_order_FSLMNI152_2mm.Centroid_RAS.csv'
        return pd.read_csv(config.MAPPING_FILES, parcel_type)

    def _get_voxels_by_roi(self, data: dict, roi: str, roi_i: int):
        pass

    def _load_data_per_subject(self):
        subjects_voxel_data = glob.glob(config.VOXEL_DATA_DF)

        for sub_file in subjects_voxel_data:
            sub_data = _load_pkl(sub_file)
            self._get_voxels_by_roi(data=sub_data, roi='name', roi_i=1)

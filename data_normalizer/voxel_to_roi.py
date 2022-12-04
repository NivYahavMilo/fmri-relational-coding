import glob
import os
from typing import Optional

import pandas as pd

import config
import data_normalizer.utils as utils
from enums import Mode


class Voxel2Roi:

    def __init__(self, mode: Mode):

        self.mode: Mode = mode
        self.network_mapping: pd.DataFrame = Optional[pd.DataFrame]
        self.voxel_mapping: pd.DataFrame = Optional[pd.DataFrame]

    def load_voxel_mapping_file(self, roi: int, nw: int, mm: int = 1):
        """
        load voxel and networks mapping by 'Schaefer2018' template.
        data members:
            network_mapping: maps ROI index to its sub network name.
            voxel_mapping: maps voxels to ROI index.
        """
        self.network_mapping = pd.read_csv(os.path.join(config.MAPPING_FILES,
                                                        config.NETWORK_MAPPING_TEMPLATE_FILE.format(roi=roi,
                                                                                                    nw=nw,
                                                                                                    mm=mm)))

        self.voxel_mapping = pd.read_csv(os.path.join(config.MAPPING_FILES,
                                                      config.VOXEL_MAPPING_FILE.format(roi=roi, nw=nw)))
        self.voxel_mapping['ROI'].astype(int)

    def _get_voxels_by_roi(self, data: pd.DataFrame, roi: str):
        """
        retrieving the voxel indices for the 'roi' input parameter.
        return:

            data frame with the relevant indices describing the chosen 'roi'.
            adding ('timepoint', 'y', 'Subject') columns to table, which describes the
            TR, Clip label and Subject id.

        """
        ROI = self.network_mapping[self.network_mapping['ROI Name'] == roi][['ROI Name', 'ROI Label']]
        roi_i = ROI['ROI Label'].apply(lambda x: x - 1).values[0]
        sub_net = ROI['ROI Name'].values[0]

        voxel_indices = self.voxel_mapping[self.voxel_mapping['ROI'] == roi_i].index.tolist()
        voxel_indices = [f'feat_{str(i)}' for i in voxel_indices]
        voxel_indices.extend(['timepoint', 'y', 'Subject'])
        masked_roi = data.loc[:, voxel_indices]
        return masked_roi

    def _save_roi_file(self, data: pd.DataFrame, roi_name: str, subject: str):
        """
        Checks if directories exists, if not saves all  ROI files to subject directory.
        mode in-charge of the navigation between resting state and task.
        """
        roi_name = roi_name.replace('7Networks_', '')
        sub_path = os.path.join(config.SUBNET_DATA_DF.format(mode=self.mode.value), subject)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)

        file_name = os.path.join(sub_path, f"{roi_name}.pkl")
        data.to_pickle(file_name)

    def load_data_per_subject(self):
        """
        Iterates subjects and retrieves the voxels per region of interest (ROI)
        save results to pkl file.
        """
        subjects_voxel_data = glob.glob(os.path.join(config.VOXEL_DATA_DF.format(mode=self.mode.value), '*.pkl'))

        for sub_file in subjects_voxel_data:
            # slice string for subject id
            sub_id = sub_file.split('.pkl')[0][-6:]
            sub_data = utils.load_pkl(sub_file)
            # get all region of interest names list
            ROIS = self.network_mapping['ROI Name'].unique()
            for r in ROIS:
                roi_data = self._get_voxels_by_roi(data=sub_data, roi=r)
                self._save_roi_file(data=roi_data, roi_name=r, subject=sub_id)
            utils.info(f"Subject {sub_id} saved")

    def flow(self):
        self.load_voxel_mapping_file(roi=300, nw=7)
        self.load_data_per_subject()

import os
import pickle

import config
import data_center.static_data.static_data as st_data
from enums import Mode
from abc import abstractmethod

class RelationalCodingBase:

    mode: Mode

    @abstractmethod
    def run(self, roi: str):
        """
        run relational coding flow.
        """
        pass

    def yield_subject_iterator(self):
        pass

    def load_roi_data(self, roi_name: str, subject: str):
        self._check_roi_validity(roi_name)

        data_path = config.SUBNET_DATA_DF.format(mode=self.mode.value)
        roi_data_p = os.path.join(data_path, subject, roi_name)
        roi_data = open(roi_data_p, 'rb')
        roi_data_df = pickle.load(roi_data)
        # release IO object from memory
        del roi_data

        return roi_data_df



    @staticmethod
    def _check_roi_validity(roi_name: str):
        if roi_name not in st_data.ROI_NAMES:
            raise ValueError("ROI name incorrect", "\n","check the following list:","\n", st_data.ROI_NAMES)

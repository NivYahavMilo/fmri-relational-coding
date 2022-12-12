from typing import Callable

from data_center.static_data.static_data import StaticData
from data_normalizer.raw_dataloader import ParcelData
from data_normalizer.split_wb_networks import Roi2Networks
from data_normalizer.voxel_to_roi import Voxel2Roi
from enums import Mode, DataType, FlowType
from relational_coding.artificial_relational_coding import ActivationsRelationalCoding
from relational_coding.fmri_relationl_coding import FmriRelationalCoding


class FlowManager:

    # load dictionary to static class members
    StaticData.inhabit_class_members()

    @classmethod
    def _step_map_voxel_to_roi(cls, *args):
        mode: Mode = args[0]
        voxel_to_roi = Voxel2Roi(mode=mode)
        voxel_to_roi.flow()

    @classmethod
    def _step_preprocess_raw_data_to_tabular(cls, *args):
        mode: Mode = args[0]
        roi: int = args[1]
        net: int = args[2]
        raw_data_parcel = ParcelData()
        raw_data_parcel.run(mode, k_roi=roi, k_net=net)

    @classmethod
    def _step_preprocess_roi_to_networks(cls, *args):
        roi_to_network = Roi2Networks()
        roi_to_network.flow()

    @classmethod
    def _step_relational_coding(cls, *args):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        avg_flag: bool = args[2]
        group: str = args[3]

        relational_coding_mapping = {
            DataType.FMRI: FmriRelationalCoding,
            DataType.ACTIVATIONS: ActivationsRelationalCoding
        }
        relation_coding = relational_coding_mapping.get(relation_coding_type)()
        relation_coding.run(roi=roi_name, avg_data=avg_flag, group=group)

    @classmethod
    def execute(cls, *args, **kwargs):

        flow_type: FlowType = kwargs['flow_type']

        flow_type_mapping = {
            FlowType.ROI_TO_NETWORK: cls._step_preprocess_roi_to_networks,
            FlowType.RAW_TO_TABULAR: cls._step_preprocess_raw_data_to_tabular,
            FlowType.VOXEL_TO_ROI: cls._step_map_voxel_to_roi,
            FlowType.RELATIONAL_CODING: cls._step_relational_coding

        }

        func_flow: Callable = flow_type_mapping.get(flow_type)
        func_flow(*args)

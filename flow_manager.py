from typing import Callable

from activtions_patterns.artifical_activations_pattern import ArtificialActivationPattern
from activtions_patterns.fmri_activations_pattern import FmriActivationPattern
from data_center.static_data.static_data import StaticData
from data_normalizer.raw_dataloader import ParcelData
from data_normalizer.split_wb_networks import Roi2Networks
from data_normalizer.voxel_to_roi import Voxel2Roi
from enums import Mode, DataType, FlowType
from relational_coding.artificial_relational_coding import ActivationsRelationalCoding
from relational_coding.custom_temporal_relational_coding import CustomTemporalRelationalCoding
from relational_coding.fmri_relationl_coding import FmriRelationalCoding
from relational_coding.singular_relational_coding import SingularRelationalCoding


class FlowManager:
    # load dictionary to static class members
    StaticData.inhabit_class_members()

    @classmethod
    def _map_voxel_to_roi(cls, *args):
        mode: Mode = args[0]
        voxel_to_roi = Voxel2Roi(mode=mode)
        voxel_to_roi.flow()

    @classmethod
    def _preprocess_raw_data_to_tabular(cls, *args):
        mode: Mode = args[0]
        roi: int = args[1]
        net: int = args[2]
        raw_data_parcel = ParcelData()
        raw_data_parcel.run(mode, k_roi=roi, k_net=net)

    @classmethod
    def _preprocess_roi_to_networks(cls, *args):
        roi_to_network = Roi2Networks()
        roi_to_network.flow()

    @classmethod
    def _relational_coding(cls, *args):
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
    def _singular_relational_coding(cls, *args):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        group: str = args[2]
        src = SingularRelationalCoding()
        src.run(roi=roi_name, group=group)

    @classmethod
    def _activations_pattern(cls, *args):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        group: str = args[2]
        relational_coding_mapping = {
            DataType.FMRI: FmriActivationPattern,
            DataType.ACTIVATIONS: ArtificialActivationPattern
        }
        relation_coding = relational_coding_mapping.get(relation_coding_type)()
        relation_coding.run(roi=roi_name, group=group)

    @classmethod
    def _custom_temporal_relational_coding(cls, *args):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        rest_window_size: tuple = args[2]
        task_window_size: int = args[3]
        custom_temporal_rc = CustomTemporalRelationalCoding()
        custom_temporal_rc.run(roi=roi_name, rest_window_size=rest_window_size, task_window_size=task_window_size)

    @classmethod
    def execute(cls, *args, **kwargs):
        flow_type: FlowType = kwargs['flow_type']

        flow_type_mapping = {
            FlowType.ROI_TO_NETWORK: cls._preprocess_roi_to_networks,
            FlowType.RAW_TO_TABULAR: cls._preprocess_raw_data_to_tabular,
            FlowType.VOXEL_TO_ROI: cls._map_voxel_to_roi,
            FlowType.RELATIONAL_CODING: cls._relational_coding,
            FlowType.ACTIVATIONS_PATTERNS: cls._activations_pattern,
            FlowType.SINGULAR_RELATIONAL_CODING: cls._singular_relational_coding,
            FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING: cls._custom_temporal_relational_coding

        }

        func_flow: Callable = flow_type_mapping.get(flow_type)
        func_flow(*args)

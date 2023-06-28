from typing import Callable

from activtions_patterns.fmri_activations_pattern import FmriActivationPattern
from data_normalizer.raw_dataloader import ParcelData
from data_normalizer.split_wb_networks import MapRoiToNetwork
from data_normalizer.voxel_extraction import VoxelExtraction
from data_normalizer.voxel_to_roi import Voxel2Roi
from enums import Mode, DataType, FlowType
from relational_coding.artificial_relational_coding import ActivationsRelationalCoding
from relational_coding.custom_temporal_relational_coding.custom_temporal_relational_coding import \
    CustomTemporalRelationalCoding
from relational_coding.custom_temporal_relational_coding.isfc_relational_coding import ISFCRelationalCoding
from relational_coding.custom_temporal_relational_coding.snr_measurements import SnrMeasurementsRelationalCoding
from relational_coding.fmri_relationl_coding import FmriRelationalCoding
from relational_coding.singular_relational_coding import SingularRelationalCoding
from relational_coding.custom_temporal_relational_coding.concat_fmri_clips import ConcatFmriTemporalRelationalCoding


class FlowManager:

    @classmethod
    def _map_voxel_to_roi(cls, *args, **kwargs):
        mode: Mode = args[0]
        voxel_to_roi = Voxel2Roi(mode=mode)
        voxel_to_roi.flow(*args, **kwargs)

    @classmethod
    def _preprocess_raw_data_to_tabular(cls, *args, **kwargs):
        mode: Mode = args[0]
        raw_data_parcel = ParcelData()
        raw_data_parcel.run(mode, **kwargs)

    @classmethod
    def _voxel_extraction(cls, *args, **kwargs):
        voxel_extraction = VoxelExtraction()
        voxel_extraction.run(*args, **kwargs)

    @classmethod
    def _preprocess_roi_to_networks(cls, *args):
        roi_to_network = MapRoiToNetwork()
        roi_to_network.flow()

    @classmethod
    def _relational_coding(cls, *args):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        avg_flag: bool = args[2]
        group: str = args[3]
        shuffle: bool = args[4]

        relational_coding_mapping = {
            DataType.FMRI: FmriRelationalCoding,
            DataType.ACTIVATIONS: ActivationsRelationalCoding
        }
        relation_coding = relational_coding_mapping.get(relation_coding_type)()
        relation_coding.run(roi=roi_name, avg_data=avg_flag, group=group, shuffle=shuffle)

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

        activation_pattern = FmriActivationPattern()
        activation_pattern.run(roi=roi_name, group=group)

    @classmethod
    def _custom_temporal_relational_coding(cls, *args, **kwargs):
        relation_coding_type: DataType = args[0]
        roi_name: str = args[1]
        rest_window_size: tuple = args[2]
        init_window_task: str = args[3]
        task_window_size: int = args[4]
        custom_temporal_rc = CustomTemporalRelationalCoding()
        custom_temporal_rc.run(
            roi=roi_name,
            rest_window_size=rest_window_size,
            init_window_task=init_window_task,
            task_window_size=task_window_size,
            **kwargs
        )

    @classmethod
    def _isfc_relational_coding(cls, *args):
        data_type: DataType = args[0]
        roi = args[1]

        isfc_rc = ISFCRelationalCoding()
        isfc_rc.run(roi=roi)

    @classmethod
    def _snr_measurement_temporal_relational_coding(cls, *args, **kwargs):
        snr_analysis = SnrMeasurementsRelationalCoding()
        snr_analysis.run(**kwargs)

    @classmethod
    def _activations_concatenated_temporal_fmri(cls, *args, **kwargs):
        activations_concat_fmri = ConcatFmriTemporalRelationalCoding()
        activations_concat_fmri.run(**kwargs)

    @classmethod
    def execute(cls, *args, **kwargs):
        flow_type: FlowType = kwargs.pop('flow_type')

        flow_type_mapping = {
            FlowType.ROI_TO_NETWORK: cls._preprocess_roi_to_networks,
            FlowType.RAW_TO_TABULAR: cls._preprocess_raw_data_to_tabular,
            FlowType.VOXEL_EXTRACTION: cls._voxel_extraction,
            FlowType.VOXEL_TO_ROI: cls._map_voxel_to_roi,
            FlowType.RELATIONAL_CODING: cls._relational_coding,
            FlowType.ACTIVATIONS_PATTERNS: cls._activations_pattern,
            FlowType.SINGULAR_RELATIONAL_CODING: cls._singular_relational_coding,
            FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING: cls._custom_temporal_relational_coding,
            FlowType.ISFC_RELATIONAL_CODING: cls._isfc_relational_coding,
            FlowType.SNR_MEASUREMENTS: cls._snr_measurement_temporal_relational_coding,
            FlowType.CONCATENATED_FMRI: cls._activations_concatenated_temporal_fmri

        }

        func_flow: Callable = flow_type_mapping.get(flow_type)
        func_flow(*args, **kwargs)

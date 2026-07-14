from typing import Callable

from data_normalizer.raw_dataloader import ParcelData
from data_normalizer.split_wb_networks import MapRoiToNetwork
from data_normalizer.voxel_extraction import VoxelExtraction
from data_normalizer.voxel_to_roi import Voxel2Roi
from enums import Mode, FlowType


class FlowManager:
    """Dispatcher for the raw-data preprocessing pipeline.

    Analysis flows no longer live here — call ``flows.<analysis>.run(...)`` directly.
    """

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
    def _preprocess_roi_to_networks(cls, *args, **kwargs):
        roi_to_network = MapRoiToNetwork()
        roi_to_network.flow(*args, **kwargs)

    @classmethod
    def execute(cls, *args, **kwargs):
        flow_type: FlowType = kwargs.pop('flow_type')

        flow_type_mapping = {
            FlowType.ROI_TO_NETWORK: cls._preprocess_roi_to_networks,
            FlowType.RAW_TO_TABULAR: cls._preprocess_raw_data_to_tabular,
            FlowType.VOXEL_EXTRACTION: cls._voxel_extraction,
            FlowType.VOXEL_TO_ROI: cls._map_voxel_to_roi,
        }

        func_flow: Callable = flow_type_mapping.get(flow_type)
        func_flow(*args, **kwargs)

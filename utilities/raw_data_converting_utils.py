from typing import List, Callable, Union

import settings
from data_center.static_data.static_data import StaticData
from data_normalizer.raw_dataloader import ParcelData
from data_normalizer.split_wb_networks import MapRoiToNetwork
from data_normalizer.voxel_extraction import VoxelExtraction
from data_normalizer.voxel_to_roi import Voxel2Roi
from enums import Mode, FlowType, ScanningMode

# Load class members from StaticData
StaticData.inhabit_class_members()


def convert_raw_data(*args, **kwargs):
    """
    Converts raw data to tabular format via ``ParcelData`` with:
    - ScanningMode.TASK
    - k_roi=300
    - k_net=7
    - z_score=False
    - save_path=settings.VOXEL_DATA_DENORMALIZED
    """
    scanning_mode: ScanningMode = kwargs.pop('scanning_mode')

    ParcelData().run(
        scanning_mode,
        k_roi=300,
        k_net=7,
        z_score=False,
        save_path=settings.VOXEL_DATA_DENORMALIZED,
    )


def extract_voxel_from_raw_data(mode: Mode, **kwargs):
    """
    Extracts voxel-level data from raw data via ``VoxelExtraction``.

    The resulting voxel data is saved under settings.VOXEL_DATA_DF_DENORMALIZED.
    """
    scanning_mode: ScanningMode = kwargs.pop('scanning_mode')

    VoxelExtraction().run(
        mode,
        scanning_mode=scanning_mode,
        save_path=settings.VOXEL_DATA_DF_DENORMALIZED,
        raw_data_path=settings.VOXEL_DATA_DENORMALIZED,
    )


def map_voxel_level_data_to_roi(mode: Mode, **kwargs):
    """
    Maps voxel-level data to ROI (Region of Interest) via ``Voxel2Roi``.

    The resulting ROI data is saved under settings.SUBNET_DATA_DF_DENORMALIZED.
    """
    Voxel2Roi(mode=mode).flow(
        mode,
        load_path=settings.VOXEL_DATA_DF_DENORMALIZED,
        save_path=settings.SUBNET_DATA_DF_DENORMALIZED,
    )


def map_rois_to_network(mode: Mode, **kwargs):
    """Aggregates ROI-level data into whole-brain networks via ``MapRoiToNetwork``."""
    MapRoiToNetwork().flow(
        mode,
        load_path=settings.NETWORK_DATA_DF_DENORMALIZED,
        save_path=settings.NETWORK_SUBNET_DATA_DF_DENORMALIZED,
    )


def data_normalizer_step_execute(steps: List[FlowType], modes: List[Union[Mode, ScanningMode]], **kwargs):
    """
    Executes the requested data-normalization steps.

    `steps_mapping` links each preprocessing ``FlowType`` to its function; for every
    requested step, the function is called once per mode.

    Parameters:
    - steps: preprocessing FlowType values to execute.
    - modes: the data modes to run each step over.
    """
    steps_mapping = {
        FlowType.RAW_TO_TABULAR: convert_raw_data,
        FlowType.VOXEL_EXTRACTION: extract_voxel_from_raw_data,
        FlowType.VOXEL_TO_ROI: map_voxel_level_data_to_roi,
        FlowType.ROI_TO_NETWORK: map_rois_to_network
    }

    for step in steps:
        for mode in modes:
            callable_step: Callable = steps_mapping.get(step)
            callable_step(mode, **kwargs)


if __name__ == '__main__':
    # Execute the data normalization steps
    data_normalizer_step_execute(steps=[
        FlowType.VOXEL_TO_ROI,

    ], scanning_mode=ScanningMode.REST, modes=[Mode.RESTING_STATE_FIRST_REST_SECTION])

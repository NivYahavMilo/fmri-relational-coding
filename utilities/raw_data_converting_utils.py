from typing import List, Callable, Union

import config
from data_center.static_data.static_data import StaticData
from enums import Mode, FlowType, ScanningMode
from flow_manager import FlowManager

# Load class members from StaticData
StaticData.inhabit_class_members()


def convert_raw_data(*args, **kwargs):
    """
    Converts raw data to tabular format.

    This function uses FlowManager to execute the conversion process from raw data to tabular format.
    The parameters used in the execution are:
    - ScanningMode.TASK
    - k_roi=300
    - k_net=7
    - z_score=False
    - save_path=config.VOXEL_DATA_DENORMALIZED
    - flow_type=FlowType.RAW_TO_TABULAR
    """

    scanning_mode: ScanningMode = kwargs.pop('scanning_mode')

    fm = FlowManager()
    fm.execute(
        scanning_mode,
        k_roi=300,
        k_net=7,
        z_score=False,
        save_path=config.VOXEL_DATA_DENORMALIZED,
        flow_type=FlowType.RAW_TO_TABULAR
    )


def extract_voxel_from_raw_data(mode: Mode, **kwargs):
    """
    Extracts voxel-level data from raw data.

    This function uses FlowManager to execute the voxel extraction process from raw data.
    It executes the process in three modes: REST, CLIPS, and FIRST_REST_SECTION.
    The resulting voxel data is saved in the config.VOXEL_DATA_DF_DENORMALIZED path.
    """
    scanning_mode: ScanningMode = kwargs.pop('scanning_mode')
    fm = FlowManager()
    fm.execute(
        mode,
        scanning_mode=scanning_mode,
        save_path=config.VOXEL_DATA_DF_DENORMALIZED,
        raw_data_path=config.VOXEL_DATA_DENORMALIZED,
        flow_type=FlowType.VOXEL_EXTRACTION
    )


def map_voxel_level_data_to_roi(mode: Mode, **kwargs):
    """
    Maps voxel-level data to ROI (Region of Interest).

    This function uses FlowManager to execute the mapping process from voxel-level data to ROI.
    It executes the process in two modes: REST and CLIPS.
    The resulting ROI data is saved in the config.SUBNET_DATA_DF_DENORMALIZED path.
    """
    fm = FlowManager()
    fm.execute(
        mode,
        load_path=config.VOXEL_DATA_DF_DENORMALIZED,
        save_path=config.SUBNET_DATA_DF_DENORMALIZED,
        flow_type=FlowType.VOXEL_TO_ROI
    )


def map_rois_to_network(mode: Mode, **kwargs):
    fm = FlowManager()
    fm.execute(
        mode,
        load_path=config.NETWORK_DATA_DF_DENORMALIZED,
        save_path=config.NETWORK_SUBNET_DATA_DF_DENORMALIZED,
        flow_type=FlowType.ROI_TO_NETWORK
    )


def data_normalizer_step_execute(steps: List[FlowType], modes: List[Union[Mode, ScanningMode]], **kwargs):
    """
    Executes the data normalization steps.

    This function takes a list of steps and executes the corresponding data normalization processes.
    The mapping between each step and the corresponding function is defined in the `steps_mapping` dictionary.
    It loops over the steps list, retrieves the corresponding function, and calls it.

    Parameters:
    - steps: A list of FlowType values representing the normalization steps to execute.
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

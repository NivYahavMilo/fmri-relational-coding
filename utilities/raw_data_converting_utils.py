import config
from data_center.static_data.static_data import StaticData
from enums import Mode, FlowType, ScanningMode
from flow_manager import FlowManager

StaticData.inhabit_class_members()


def convert_raw_data():
    fm = FlowManager()
    fm.execute(
        ScanningMode.TASK,
        k_roi=300,
        k_net=7,
        z_score=False,
        save_path=config.VOXEL_DATA_DENORMALIZED,
        flow_type=FlowType.RAW_TO_TABULAR
    )


def extract_voxel_from_raw_data():
    fm = FlowManager()
    fm.execute(Mode.REST, save_path=config.VOXEL_DATA_DF_DENORMALIZED, raw_data_path=config.VOXEL_DATA_DENORMALIZED,
               flow_type=FlowType.VOXEL_EXTRACTION)

    fm.execute(Mode.CLIPS, save_path=config.VOXEL_DATA_DF_DENORMALIZED, raw_data_path=config.VOXEL_DATA_DENORMALIZED,
               flow_type=FlowType.VOXEL_EXTRACTION)


def map_voxel_level_data_to_roi():
    fm = FlowManager()
    fm.execute(Mode.REST, load_path=config.VOXEL_DATA_DF_DENORMALIZED, save_path=config.SUBNET_DATA_DF_DENORMALIZED,
               flow_type=FlowType.VOXEL_TO_ROI)
    fm.execute(Mode.CLIPS, load_path=config.VOXEL_DATA_DF_DENORMALIZED, save_path=config.SUBNET_DATA_DF_DENORMALIZED,
               flow_type=FlowType.VOXEL_TO_ROI)


if __name__ == '__main__':
    convert_raw_data()
    extract_voxel_from_raw_data()
    map_voxel_level_data_to_roi()

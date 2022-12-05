from data_center.static_data.static_data import StaticData
from enums import DataType, FlowType
from flow_manager import FlowManager

def relation_coding_for_all_roi():
    for roi in StaticData.ROI_NAMES[::-1]:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, flow_type=FlowType.RELATIONAL_CODING)
        del fm


def relation_coding_for_specific_roi(roi):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, flow_type=FlowType.RELATIONAL_CODING)

if __name__ == '__main__':
    #relation_coding_for_specific_roi("RH_Default_pCunPCC_3")
    relation_coding_for_all_roi()
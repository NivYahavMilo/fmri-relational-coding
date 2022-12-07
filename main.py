from data_center.static_data.static_data import StaticData
from enums import DataType, FlowType
from flow_manager import FlowManager
from visualizations.plot_relational_coding import plot_pipe

def relation_coding_for_all_roi(with_plot: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, flow_type=FlowType.RELATIONAL_CODING)
        del fm

        if with_plot:
            plot_pipe(roi)


def relation_coding_for_specific_roi(roi, with_plot: bool = False):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, flow_type=FlowType.RELATIONAL_CODING)
    if with_plot:
        plot_pipe(roi)


if __name__ == '__main__':
    # relation_coding_for_specific_roi("RH_Default_pCunPCC_3", with_plot=True)
    relation_coding_for_all_roi(with_plot=True)
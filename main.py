import visualizations.plot_relational_coding as plot
from data_center.static_data.static_data import StaticData
from enums import DataType, FlowType
from flow_manager import FlowManager


def relation_coding_for_all_roi(avg_data: bool = False, with_plot: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, avg_data, flow_type=FlowType.RELATIONAL_CODING)
        del fm

        if with_plot:
            if avg_data:
                plot.plot_pipe_avg(roi)
            else:
                plot.plot_pipe(roi)


def relation_coding_for_specific_roi(roi, avg_data: bool = False, with_plot: bool = False):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, avg_data, flow_type=FlowType.RELATIONAL_CODING)
    if with_plot:
        if avg_data:
            plot.plot_pipe_avg(roi)
        else:
            plot.plot_pipe(roi)


if __name__ == '__main__':
    #relation_coding_for_specific_roi("RH_SomMot_6", avg_data=False, with_plot=True)
    relation_coding_for_all_roi(avg_data=True, with_plot=False)

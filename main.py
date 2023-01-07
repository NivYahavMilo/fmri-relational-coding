from data_center.static_data.static_data import StaticData
from enums import DataType, FlowType
from flow_manager import FlowManager

import visualizations.plot_relational_coding as plot
import visualizations.plot_temporal_relational_coding_window as plot_window

def relation_coding_for_all_roi(avg_data: bool = False, with_plot: bool = False, group: str = ''):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, avg_data, group, flow_type=FlowType.RELATIONAL_CODING)
        del fm

        if with_plot:
            if avg_data:
                plot.plot_pipe_avg(roi, group)
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


def activations_pattern_for_all_roi(group, with_plot: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, group, flow_type=FlowType.ACTIVATIONS_PATTERNS)
        del fm
        if with_plot:
            plot.plot_activation_pattern(roi, group)


def activations_pattern_for_specific_roi(roi, group, with_plot: bool = False):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, group, flow_type=FlowType.ACTIVATIONS_PATTERNS)
    if with_plot:
        plot.plot_activation_pattern(roi, group)


def singular_relational_coding(group, with_plot: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, group, flow_type=FlowType.SINGULAR_RELATIONAL_CODING)
        del fm


def singular_relational_coding_for_specific_roi(roi, group, with_plot: bool = False):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, group, flow_type=FlowType.SINGULAR_RELATIONAL_CODING)


def custom_temporal_relational_coding_for_specific_roi(roi, rest_ws, task_ws, with_plot: bool = False):
    fm = FlowManager()
    fm.execute(DataType.FMRI, roi, rest_ws, task_ws, flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING)
    if with_plot:
        plot.custom_window_rc_histogram(roi=roi, rest_window=rest_ws, task_window=task_ws)


def custom_temporal_relational_coding(rest_ws, task_ws, with_plot: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, rest_ws, task_ws, flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING)
        del fm

        if with_plot:
            plot.custom_window_rc_histogram(roi=roi, rest_window=rest_ws, task_window=task_ws)


def moving_window_custom_temporal_relational_coding(with_plot):
    task_ws = 10
    rest_s, rest_e = (0, 5)
    while rest_e < 19:
        rest_ws = rest_s, rest_e
        for roi in StaticData.ROI_NAMES:
            fm = FlowManager()
            fm.execute(DataType.FMRI, roi, rest_ws, task_ws, flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING)
            del fm

        print(f'Done window {rest_ws}')
        rest_s += 1
        rest_e += 1

    if with_plot:
        plot_window.window_relational_coding_plot(show=True, save_img=True)


if __name__ == '__main__':
    # relation_coding_for_specific_roi("RH_SomMot_6", avg_data=False, with_plot=True)
    # relation_coding_for_all_roi(avg_data=True, with_plot=True, group='_GROUP2')
    # relation_coding_for_all_roi(avg_data=True, with_plot=True, group='_GROUP1')
    # activations_pattern_for_specific_roi('RH_Default_pCunPCC_6', group='_GROUP2', with_plot=True)
    # activations_pattern_for_all_roi(group='', with_plot=True)
    # singular_relational_coding_for_specific_roi('RH_Default_pCunPCC_6', group='')
    # custom_temporal_relational_coding_for_specific_roi(roi='RH_Vis_18',rest_ws=(8, 13), task_ws=10, with_plot=False)
    # custom_temporal_relational_coding(rest_ws=(6, 16), task_ws=10, with_plot=True)
    moving_window_custom_temporal_relational_coding(with_plot=True)

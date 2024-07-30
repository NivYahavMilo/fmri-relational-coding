import visualizations.plot_relational_coding as plot
import visualizations.plot_snr_measurement as plot_snr
import visualizations.plot_temporal_relational_coding_window as plot_window
from data_center.static_data.static_data import StaticData
from enums import DataType, FlowType
from flow_manager import FlowManager

# load dictionary to static class members
StaticData.inhabit_class_members()


def relation_coding_for_all_roi(avg_data: bool = False, with_plot: bool = False, group: str = '',
                                shuffle: bool = False):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, avg_data, group, shuffle, flow_type=FlowType.RELATIONAL_CODING)
        del fm

        if with_plot:
            if avg_data:
                plot.plot_pipe_avg(roi, group, shuffle)
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


def moving_window_custom_temporal_relational_coding(**kwargs):
    if isinstance(kwargs.get('roi'), list):
        rois = kwargs.pop('roi')

    elif kwargs.get('roi'):
        rois = [kwargs.pop('roi')]

    else:
        rois = StaticData.ROI_NAMES

    avg_data = kwargs.get('average_data')
    for init_window in ['end']:
        task_ws = 10
        rest_s, rest_e = (0, 5)
        while rest_e < 30:
            rest_ws = rest_s, rest_e
            for roi in rois:
                fm = FlowManager()
                fm.execute(DataType.FMRI, roi, rest_ws, init_window, task_ws,
                           flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING, **kwargs)
                del fm

            print('done window', rest_ws)
            rest_s += 1
            rest_e += 1

        if kwargs.get('with_plot'):
            plot_window.window_relational_coding_plot(task_window=init_window, show=True, save_img=True,
                                                      avg_data=avg_data, roi=rois)
    if kwargs.get('with_bar'):
        plot_window.window_average_rc_bar_plot(avg_data=avg_data, with_shuffle=True, save_img=True)


def isfc_relational_coding(with_plot=None):
    for roi in StaticData.ROI_NAMES:
        fm = FlowManager()
        fm.execute(DataType.FMRI, roi, flow_type=FlowType.ISFC_RELATIONAL_CODING)
        del fm

        if with_plot:
            plot.plot_pipe(roi)


def moving_window_custom_temporal_relational_coding_with_signal_processing(
        roi,
        average_data,
        shuffle,
        filtering,
        decomposition,
        with_plot
):
    for init_window in ['end']:
        task_ws = 10
        rest_s, rest_e = (0, 5)
        while rest_e < 19:
            rest_ws = rest_s, rest_e
            # for roi in StaticData.ROI_NAMES:
            fm = FlowManager()
            fm.execute(
                DataType.FMRI,
                roi,
                rest_ws,
                init_window,
                task_ws,
                avg_data=average_data,
                shuffle_rest=shuffle,
                filtering=filtering,
                decomposition=decomposition,
                filter_order=10,
                filter_cut_off=0.09,
                flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING
            )
            del fm
            rest_s += 1
            rest_e += 1
            print(rest_ws)
        if with_plot:
            plot_window.window_relational_coding_plot(
                roi=roi,
                task_window=init_window,
                mode='pca' if decomposition else 'filtering',
                show=True,
                save_img=True,
                avg_data=average_data,
                filter_order=30,
                filter_cut_off=0.3,
            )


def snr_measurement(**kwargs):
    rois = kwargs.get('roi')

    if rois and not isinstance(rois, list):
        rois = [kwargs.get('roi')]

    elif not rois:
        rois = StaticData.ROI_NAMES

    for init_window in ['end']:
        for group_index in [1, 2, 3, 4, 5, 6]:
            task_ws = 10
            rest_s, rest_e = (0, 5)
            while rest_e < 19:
                rest_ws = rest_s, rest_e
                for roi in rois:
                    fm = FlowManager()
                    fm.execute(
                        DataType.FMRI,
                        roi=roi,
                        rest_ws=rest_ws,
                        init_window=init_window,
                        window_moving_size=10,
                        # window_range=(10,20),
                        task_ws=task_ws,
                        group_index=group_index,
                        group_subjects=10,
                        skip_correlation=False,
                        movie_distances=True,
                        movie_activation=False,
                        shuffle_rest=False,
                        flow_type=FlowType.SNR_MEASUREMENTS
                        )
                del fm
                rest_s += 1
                rest_e += 1




            print('done group i', group_index)
        print('done window', init_window)

        if kwargs.get('plot'):
            plot_snr.plot_snr_measurement(
                group_index,
                save_figure=False,
                plot_combined_groups=True,
                plot_heatmap=False,
                max=True
            )


if __name__ == '__main__':
    # relation_coding_for_specific_roi()
    # relation_coding_for_all_roi(avg_data=True, with_plot=True, group='_GROUP2')
    # relation_coding_for_all_roi(avg_data=True, with_plot=True, group='_GROUP1')
    # activations_pattern_for_specific_roi('RH_Default_pCunPCC_6', group='_GROUP2', with_plot=True)
    # activations_pattern_for_all_roi(group='', with_plot=True)
    # singular_relational_coding_for_specific_roi('RH_Default_pCunPCC_6', group='')
    # custom_temporal_relational_coding_for_specific_roi(roi='RH_Vis_18',rest_ws=(8, 13), task_ws=10, with_plot=False)
    # custom_temporal_relational_coding(rest_ws=(6, 16), task_ws=10, with_plot=True)
    # moving_window_custom_temporal_relational_coding(with_plot=True)

    # relation_coding_for_all_roi(avg_data=True, shuffle=True, with_plot=True)

    # moving_window_custom_temporal_relational_coding(average_data=True, shuffle=True, with_plot=False, with_bar=False)
    # moving_window_custom_temporal_relational_coding(average_data=False, shuffle=True, with_plot=False, with_bar=False)
    # moving_window_custom_temporal_relational_coding_with_signal_processing(
    #     roi='',
    #     average_data=False,
    #     shuffle=False,
    #     filtering=False,
    #     decomposition=True,
    #     with_plot=True,
    # )

    # moving_window_custom_temporal_relational_coding_with_signal_processing(
    #     roi='RH_Default_Temp_6',
    #     average_data=False,
    #     shuffle=False,
    #     filtering=True,
    #     decomposition=False,
    #     with_plot=True
    # )
    # isfc_relational_coding(with_plot=1)
    snr_measurement(roi='RH_DorsAttn_Post_2')
    #     # activations_pattern_for_specific_roi(roi='RH_Default_pCunPCC_1', group='_GROUP2', with_plot=True)
    moving_window_custom_temporal_relational_coding(
        # roi=['RH_Default_pCunPCC_1', 'LH_Default_PFC_15', 'RH_Default_Par_1'],
        average_data=True,
        shuffle=False,
        with_plot=True,
        with_bar=False
    )
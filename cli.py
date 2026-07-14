"""Command-line interface for the relational-coding analyses.

Each subcommand maps to a launcher in ``main.py`` (which composes the ``flows/``
modules). Run one analysis at a time:

    python -m cli relational-coding --roi RH_Vis_18 --avg --plot
    python -m cli custom-temporal --rest-start 6 --rest-end 16 --task-ws 10
    python -m cli isfc --plot

Omitting ``--roi`` runs the analysis over every ROI in ``StaticData.ROI_NAMES``.
Analyses read/write data under the paths configured in ``settings.py`` (see
``.env.example``); a full run therefore needs the preprocessed HCP tables on disk.
"""
import argparse

import main


def _run_relational_coding(args):
    if args.roi:
        main.relation_coding_for_specific_roi(args.roi, avg_data=args.avg, with_plot=args.plot)
    else:
        main.relation_coding_for_all_roi(avg_data=args.avg, with_plot=args.plot,
                                         group=args.group, shuffle=args.shuffle)


def _run_singular(args):
    if args.roi:
        main.singular_relational_coding_for_specific_roi(args.roi, args.group, with_plot=args.plot)
    else:
        main.singular_relational_coding(args.group, with_plot=args.plot)


def _run_activations(args):
    if args.roi:
        main.activations_pattern_for_specific_roi(args.roi, args.group, with_plot=args.plot)
    else:
        main.activations_pattern_for_all_roi(args.group, with_plot=args.plot)


def _run_custom_temporal(args):
    rest_ws = (args.rest_start, args.rest_end)
    if args.roi:
        main.custom_temporal_relational_coding_for_specific_roi(
            args.roi, rest_ws=rest_ws, task_ws=args.task_ws, with_plot=args.plot)
    else:
        main.custom_temporal_relational_coding(rest_ws=rest_ws, task_ws=args.task_ws, with_plot=args.plot)


def _run_moving_window(args):
    kwargs = dict(average_data=args.avg, shuffle=args.shuffle,
                  with_plot=args.plot, with_bar=args.bar)
    if args.roi:
        kwargs['roi'] = args.roi
    main.moving_window_custom_temporal_relational_coding(**kwargs)


def _run_moving_window_sp(args):
    main.moving_window_custom_temporal_relational_coding_with_signal_processing(
        roi=args.roi or '',
        average_data=args.avg,
        shuffle=args.shuffle,
        filtering=args.filtering,
        decomposition=args.decomposition,
        with_plot=args.plot,
    )


def _run_isfc(args):
    main.isfc_relational_coding(with_plot=args.plot)


def _run_snr(args):
    main.snr_measurement(roi=args.roi, plot=args.plot)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="fmri-relational-coding",
        description="Run relational-coding analyses over HCP movie/rest fMRI data.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_roi(p, help_="ROI name; omit to run over all ROIs"):
        p.add_argument("--roi", default=None, help=help_)

    def add_plot(p):
        p.add_argument("--plot", action="store_true", help="render figures after the run")

    # relational-coding
    p = sub.add_parser("relational-coding", help="task-vs-rest relational distance across rest TRs")
    add_roi(p)
    p.add_argument("--avg", action="store_true", help="use group-averaged data")
    p.add_argument("--group", default="", help="group suffix for averaged data, e.g. _GROUP1")
    p.add_argument("--shuffle", action="store_true", help="permutation control (shuffle rest)")
    add_plot(p)
    p.set_defaults(handler=_run_relational_coding)

    # singular
    p = sub.add_parser("singular", help="task end-TR vs averaged-rest relational coding")
    add_roi(p)
    p.add_argument("--group", default="", help="group suffix, e.g. _GROUP1")
    add_plot(p)
    p.set_defaults(handler=_run_singular)

    # activations
    p = sub.add_parser("activations", help="activation-pattern correlations")
    add_roi(p)
    p.add_argument("--group", default="", help="group suffix, e.g. _GROUP2")
    add_plot(p)
    p.set_defaults(handler=_run_activations)

    # custom-temporal
    p = sub.add_parser("custom-temporal", help="sliding task/rest window relational coding")
    add_roi(p)
    p.add_argument("--rest-start", type=int, required=True, help="rest window start TR")
    p.add_argument("--rest-end", type=int, required=True, help="rest window end TR")
    p.add_argument("--task-ws", type=int, default=10, help="task window size (TRs)")
    add_plot(p)
    p.set_defaults(handler=_run_custom_temporal)

    # moving-window
    p = sub.add_parser("moving-window", help="custom-temporal swept over rest windows")
    p.add_argument("--roi", action="append", default=None,
                   help="ROI name; repeat for several, omit for all ROIs")
    p.add_argument("--avg", action="store_true", help="use group-averaged data")
    p.add_argument("--shuffle", action="store_true", help="permutation control (shuffle rest)")
    add_plot(p)
    p.add_argument("--bar", action="store_true", help="also render the averaged bar plot")
    p.set_defaults(handler=_run_moving_window)

    # moving-window-sp
    p = sub.add_parser("moving-window-sp",
                       help="moving-window with signal processing (filtering / PCA)")
    add_roi(p)
    p.add_argument("--avg", action="store_true", help="use group-averaged data")
    p.add_argument("--shuffle", action="store_true", help="permutation control (shuffle rest)")
    p.add_argument("--filtering", action="store_true", help="apply low-pass filtering")
    p.add_argument("--decomposition", action="store_true", help="apply PCA decomposition")
    add_plot(p)
    p.set_defaults(handler=_run_moving_window_sp)

    # isfc
    p = sub.add_parser("isfc", help="inter-subject functional correlation relational coding")
    add_plot(p)
    p.set_defaults(handler=_run_isfc)

    # snr
    p = sub.add_parser("snr", help="SNR / movie-distance measurements over subject groups")
    add_roi(p)
    add_plot(p)
    p.set_defaults(handler=_run_snr)

    return parser


def run(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.handler(args)


if __name__ == "__main__":
    run()

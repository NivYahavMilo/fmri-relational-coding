"""CLI wiring: argument parsing and subcommand -> handler dispatch (no analysis is executed)."""
import pytest

import cli


def _parse(argv):
    return cli.build_parser().parse_args(argv)


def test_requires_a_subcommand():
    with pytest.raises(SystemExit):
        _parse([])


def test_unknown_subcommand_errors():
    with pytest.raises(SystemExit):
        _parse(["does-not-exist"])


def test_relational_coding_specific_roi():
    args = _parse(["relational-coding", "--roi", "RH_Vis_18", "--avg", "--plot"])
    assert args.handler is cli._run_relational_coding
    assert args.roi == "RH_Vis_18"
    assert args.avg is True and args.plot is True
    assert args.shuffle is False and args.group == ""


def test_relational_coding_all_roi_defaults():
    args = _parse(["relational-coding"])
    assert args.roi is None
    assert args.avg is False and args.plot is False and args.shuffle is False


def test_singular_and_activations_take_group():
    s = _parse(["singular", "--roi", "RH_Vis_1", "--group", "_GROUP1"])
    assert s.handler is cli._run_singular and s.group == "_GROUP1"
    a = _parse(["activations", "--group", "_GROUP2", "--plot"])
    assert a.handler is cli._run_activations and a.roi is None and a.plot is True


def test_custom_temporal_builds_window_and_requires_bounds():
    args = _parse(["custom-temporal", "--rest-start", "6", "--rest-end", "16", "--task-ws", "10"])
    assert args.handler is cli._run_custom_temporal
    assert (args.rest_start, args.rest_end) == (6, 16)
    assert args.task_ws == 10
    # rest bounds are required
    with pytest.raises(SystemExit):
        _parse(["custom-temporal", "--rest-start", "6"])


def test_custom_temporal_task_ws_default():
    args = _parse(["custom-temporal", "--rest-start", "0", "--rest-end", "5"])
    assert args.task_ws == 10


def test_moving_window_roi_is_repeatable_list():
    args = _parse(["moving-window", "--roi", "A", "--roi", "B", "--avg", "--bar"])
    assert args.handler is cli._run_moving_window
    assert args.roi == ["A", "B"]
    assert args.avg is True and args.bar is True
    # omitted -> None (launcher then sweeps all ROIs)
    assert _parse(["moving-window"]).roi is None


def test_moving_window_sp_flags():
    args = _parse(["moving-window-sp", "--roi", "RH_Default_Temp_6", "--filtering", "--plot"])
    assert args.handler is cli._run_moving_window_sp
    assert args.filtering is True and args.decomposition is False and args.plot is True


def test_isfc_and_snr():
    i = _parse(["isfc", "--plot"])
    assert i.handler is cli._run_isfc and i.plot is True
    s = _parse(["snr", "--roi", "RH_DorsAttn_Post_2"])
    assert s.handler is cli._run_snr and s.roi == "RH_DorsAttn_Post_2" and s.plot is False

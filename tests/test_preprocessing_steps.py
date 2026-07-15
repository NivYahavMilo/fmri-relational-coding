"""Preprocessing step wiring + enum surface after removing FlowManager."""
import enums


def test_flowtype_only_has_preprocessing_steps():
    # The analysis FlowType members were dropped when FlowManager's analysis path
    # was removed; only the four preprocessing steps remain.
    assert {m.name for m in enums.FlowType} == {
        "ROI_TO_NETWORK", "VOXEL_TO_ROI", "RAW_TO_TABULAR", "VOXEL_EXTRACTION",
    }


def test_datatype_enum_removed():
    # DataType was unused after the refactor and has been deleted.
    assert not hasattr(enums, "DataType")


def test_flowmanager_module_gone():
    import importlib
    import pytest
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("flow_manager")


def test_preprocessing_util_exposes_the_four_steps():
    from utilities import raw_data_converting_utils as rdc
    for name in ("convert_raw_data", "extract_voxel_from_raw_data",
                 "map_voxel_level_data_to_roi", "map_rois_to_network"):
        assert callable(getattr(rdc, name))

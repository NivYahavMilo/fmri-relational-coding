from enum import Enum, auto


class Mode(Enum):
    CLIPS = 'TASK'
    REST = 'REST'


class Network(Enum):
    WB = 'whole brain'
    Visual = 'VisualNetwork'
    Limbic = 'Limbic'
    Somatomotor = 'SomMotor'
    DorsalAttention = 'DorsalAttention'
    VentralAttention = 'SalVenAttn'
    Default = 'DMN'
    Frontoparietal = 'Cont'


class DataType(Enum):
    FMRI = 'fMRI'
    ACTIVATIONS = 'LSTM PATTERNS'


class FlowType(Enum):
    ROI_TO_NETWORK = auto()
    VOXEL_TO_ROI = auto()
    RAW_TO_TABULAR = auto()
    RELATIONAL_CODING = auto()
    ACTIVATIONS_PATTERNS = auto()
    SINGULAR_RELATIONAL_CODING = auto()
    CUSTOM_TEMPORAL_RELATIONAL_CODING = auto()

from enum import Enum


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

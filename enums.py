from enum import Enum, auto


class ScanningMode(Enum):
    REST = 'rest'
    TASK = 'task'


class Mode(Enum):
    CLIPS = 'TASK'
    REST = 'REST'
    FIRST_REST_SECTION = 'FIRST_REST_SECTION'
    RESTING_STATE_TASK = 'RESTING_STATE_TASK'
    RESTING_STATE_REST = 'RESTING_STATE_REST'
    RESTING_STATE_FIRST_REST_SECTION = 'RESTING_STATE_FIRST_REST_SECTION'


class Network(Enum):
    WB = 'whole brain'
    Visual = 'VisualNetwork'
    Limbic = 'Limbic'
    Somatomotor = 'SomMotor'
    DorsalAttention = 'DorsalAttention'
    VentralAttention = 'SalVenAttn'
    Default = 'DMN'
    Frontoparietal = 'Cont'


class FlowType(Enum):
    # Preprocessing pipeline steps (see utilities/raw_data_converting_utils.py).
    # Analysis flows are no longer dispatched via enums — call flows.<analysis>.run(...).
    ROI_TO_NETWORK = auto()
    VOXEL_TO_ROI = auto()
    RAW_TO_TABULAR = auto()
    VOXEL_EXTRACTION = auto()


class AnalysisType(Enum):
    RELATIONAL_CODING = 'Correlations'
    RESTING_STATE_RELATIONAL_CODING = 'Resting State Correlations'
    RESTING_STATE_ACTIVATIONS_PATTERNS = 'Resting State Activations'
    ACTIVATIONS_PATTERNS = 'Activations'
    SINGLE_MOVIE_ACTIVATION = 'Single Movie Activation'
    MOVIE_DISTANCES = 'Movie Distances'

import os

ROOT_PATH = os.path.abspath(os.path.curdir)
DATA_CENTER = os.path.join(ROOT_PATH, 'data_center')
STATIC_DATA_PATH = os.path.join(ROOT_PATH, 'data_center', 'static_data')
MAPPING_FILES = os.path.join(ROOT_PATH, 'data_center', 'mappings')
TIMING_FILES = os.path.join(ROOT_PATH, 'data_center', 'timing_files')
RAW_DATA = os.path.join(r'E:', 'S1200', '7T_{mode}')
DATA_DRIVE_E = os.path.join(r'E:', 'parcelled_data_niv')
VOXEL_DATA = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL')
VOXEL_DATA_DF = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL_{mode}_DF')
SUBNET_DATA_DF = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_{mode}_DF')
SUBNET_DATA_AVG = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_AVG_{mode}{group}')

FMRI_ACTIVATIONS_PATTERN_RESULTS = os.path.join(ROOT_PATH, 'results', 'activations_patterns', 'activations_patterns')
FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG = os.path.join(ROOT_PATH, 'results', 'activations_patterns','activations_patterns{group}')
FMRI_ACTIVATIONS_PATTERN_RESULTS_FIGURES = os.path.join(ROOT_PATH, 'results', 'activations_patterns', 'activations_patterns_figures{group}')

FMRI_RELATION_CODING_RESULTS = os.path.join(ROOT_PATH, 'results', 'relational_coding', 'relational_coding')
FMRI_RELATION_CODING_RESULTS_AVG = os.path.join(ROOT_PATH, 'results', 'relational_coding', 'relational_coding_avg{group}')
FMRI_RELATION_CODING_RESULTS_FIGURES = os.path.join(ROOT_PATH, 'results', 'relational_coding', 'figures{group}')

FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS = os.path.join(ROOT_PATH, 'results', 'relational_coding', 'custom_temporal_relational_coding', '{range}')
FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES = os.path.join(ROOT_PATH, 'results', 'relational_coding','custom_temporal_relational_coding','figures')
K_GRAYORIDNATES = 59412

NETWORK_MAPPING_TEMPLATE_FILE = r'Schaefer2018_{roi}Parcels_{nw}Networks_order_FSLMNI152_{mm}mm.Centroid_RAS.csv'

VOXEL_MAPPING_FILE = r'Schaefer2018_{roi}Parcels_{nw}Networks_order.csv'

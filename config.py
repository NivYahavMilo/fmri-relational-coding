import os

""" Repository paths """
ROOT_PATH = os.path.abspath(os.path.curdir)
DATA_CENTER = os.path.join(ROOT_PATH, 'data_center')
STATIC_DATA_PATH = os.path.join(ROOT_PATH, 'data_center', 'static_data')
MAPPING_FILES = os.path.join(ROOT_PATH, 'data_center', 'mappings')
TIMING_FILES = os.path.join(ROOT_PATH, 'data_center', 'timing_files')

""" External Data Source path """
RAW_DATA = os.path.join(r'E:', 'S1200', '7T_{mode}')
DATA_DRIVE_E = os.path.join(r'E:', 'parcelled_data_niv')
RESULTS_DIR = os.path.join(r'E:', 'fmri-relational-coding-results')
VOXEL_DATA = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL')
VOXEL_DATA_RESTING_STATE = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL_RESTING_STATE')

VOXEL_DATA_DF = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL_{mode}_DF')
SUBNET_DATA_DF = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_{mode}_DF')
SUBNET_DATA_AVG = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_AVG_{mode}{group}')
SUBJECTS_AVG_DATA_LEAVE_ONE_OUT = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_AVG_LEAVE_ONE_OUT_REST')
SUBNET_AVG_N_SUBJECTS = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_AVG_N_SUBJECTS_{mode}',
                                     'AVG_{n_subjects}_SUBJECTS', 'GROUP_{group_i}')

# Raw data denormalized (without zscore)
VOXEL_DATA_DENORMALIZED = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL_denormalized')
VOXEL_DATA_DF_DENORMALIZED = os.path.join(DATA_DRIVE_E, 'schaefer2018_VOXEL_{mode}_DF_denormalized')
SUBNET_DATA_DF_DENORMALIZED = os.path.join(DATA_DRIVE_E, 'Schaefer2018_SUBNET_{mode}_DF_denormalized')

""" Results paths """
ACTIVATIONS_PATTERN = os.path.join(RESULTS_DIR, 'activations_patterns')
RELATIONAL_CODING = os.path.join(RESULTS_DIR, 'relational_coding')

FMRI_ACTIVATIONS_PATTERN_RESULTS = os.path.join(ACTIVATIONS_PATTERN, 'activations_patterns')
FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG = os.path.join(ACTIVATIONS_PATTERN, 'activations_patterns{group}')
FMRI_ACTIVATIONS_PATTERN_RESULTS_FIGURES = os.path.join(ACTIVATIONS_PATTERN, 'activations_patterns_figures{group}')

FMRI_SINGLE_MOVIE_ACTIVATIONS_PATTERN_RESULTS = os.path.join(ACTIVATIONS_PATTERN, 'single_movie_activation',
                                                             '{group_amount}_subjects_average', 'group_{group_index}',
                                                             '{range}')

CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_SUBJECT = os.path.join(ACTIVATIONS_PATTERN, 'concat_signals')
CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_ = os.path.join(ACTIVATIONS_PATTERN, 'concat_signals_avg')
CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS = os.path.join(ACTIVATIONS_PATTERN,
                                                                     'concat_signals_resting_state')
CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_SINGLE = os.path.join(CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_SUBJECT,
                                                              '{range}')
CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG = os.path.join(CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_,
                                                           '{group_amount}_subjects_average', 'group_{group_index}',
                                                           '{range}')
CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_FIGURES = os.path.join(CONCAT_FMRI_ACTIVATIONS_PATTERN_RESULTS_,
                                                               'activations_patterns_figures{group}')

CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS_AVG = os.path.join(
    CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS, '{group_amount}_subjects_average', 'group_{group_index}',
    '{range}')
CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS_FIGURES = os.path.join(
    CONCAT_RESTING_STATE_FMRI_ACTIVATIONS_PATTERN_RESULTS, 'activations_patterns_figures{group}')

FMRI_RELATION_CODING_RESULTS = os.path.join(RELATIONAL_CODING, 'relational_coding')
FMRI_RELATION_CODING_RESULTS_AVG = os.path.join(RELATIONAL_CODING, 'relational_coding_avg{group}')
FMRI_RELATION_CODING_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING, 'figures{group}')

FMRI_RELATION_CODING_SHUFFLE_REST_RESULTS = os.path.join(RELATIONAL_CODING, 'relational_coding_shuffle_rest')
FMRI_RELATION_CODING_SHUFFLE_REST_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING, 'figures_shuffle_rest')

FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS = os.path.join(RELATIONAL_CODING, 'custom_temporal_relational_coding',
                                                            '{range}')
FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING,
                                                                           'custom_temporal_relational_coding',
                                                                           'figures', '{task_window}_task_window')

FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_FILTERING = os.path.join(RELATIONAL_CODING,
                                                                      'custom_temporal_relational_coding_filtering',
                                                                      '{range}')
FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_FILTERING_FIGURES = os.path.join(RELATIONAL_CODING,
                                                                              'custom_temporal_relational_coding_filtering',
                                                                              'figures', '{task_window}_task_window')

FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_PCA = os.path.join(RELATIONAL_CODING,
                                                                'custom_temporal_relational_coding_pca', '{range}')
FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_PCA_FIGURES = os.path.join(RELATIONAL_CODING,
                                                                        'custom_temporal_relational_coding_pca',
                                                                        'figures', '{task_window}_task_window')

FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG = os.path.join(RELATIONAL_CODING,
                                                                'custom_temporal_relational_coding_avg', '{range}')
FMRI_CUSTOM_TEMPORAL_RELATION_CODING_WINDOW_RESULTS_AVG_FIGURES = os.path.join(RELATIONAL_CODING,
                                                                               'custom_temporal_relational_coding_avg',
                                                                               'figures', '{task_window}_task_window')

ISFC_RELATIONAL_CODING_RESULTS = os.path.join(RELATIONAL_CODING, 'isfc_relational_coding')
ISFC_RELATIONAL_CODING_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING, 'isfc_relational_coding_figures')

SNR_RELATIONAL_CODING_RESULTS = os.path.join(RELATIONAL_CODING, 'snr_relational_coding',
                                             '{group_amount}_subjects_average', 'group_{group_index}', '{range}')
SNR_RELATIONAL_CODING_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING, 'snr_relational_coding',
                                                     'snr_relational_coding_figures', 'group_{group_index}')

SNR_RESTING_STATE_RELATIONAL_CODING_RESULTS = os.path.join(RELATIONAL_CODING, 'snr_relational_coding_resting_state',
                                                           '{group_amount}_subjects_average', 'group_{group_index}',
                                                           '{range}')
SNR_RESTING_STATE_RELATIONAL_CODING_RESULTS_FIGURES = os.path.join(RELATIONAL_CODING,
                                                                   'snr_relational_coding_resting_state',
                                                                   'snr_relational_coding_figures',
                                                                   'group_{group_index}')

MOVIE_DISTANCES_CORRELATION_ANALYSIS = os.path.join(RELATIONAL_CODING, 'movie_distances_correlation',
                                                    '{group_amount}_subjects_average', 'group_{group_index}', '{range}')

ARTICLE_FIGURES_PATH = os.path.join(RESULTS_DIR, 'figures')
ARTICLE_FIGURES_PATH_ACTIVATIONS = os.path.join(ARTICLE_FIGURES_PATH, 'activations')
ARTICLE_FIGURES_PATH_RESTING_STATE_ACTIVATIONS = os.path.join(ARTICLE_FIGURES_PATH, 'resting_state_activations')
ARTICLE_FIGURES_PATH_CORRELATIONS = os.path.join(ARTICLE_FIGURES_PATH, 'correlations')
ARTICLE_FIGURES_PATH_RESTING_STATE_CORRELATIONS = os.path.join(ARTICLE_FIGURES_PATH, 'resting_state_correlations')

K_GRAYORIDNATES = 59412

K_SUBJECTS = 176

NETWORK_MAPPING_TEMPLATE_FILE = r'Schaefer2018_{roi}Parcels_{nw}Networks_order_FSLMNI152_{mm}mm.Centroid_RAS.csv'

VOXEL_MAPPING_FILE = r'Schaefer2018_{roi}Parcels_{nw}Networks_order.csv'

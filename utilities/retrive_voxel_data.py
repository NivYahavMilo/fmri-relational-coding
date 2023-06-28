import os

import matplotlib.pyplot as plt
import pandas as pd

import config
from arithmetic_operations.correlation_and_standartization import z_score
from data_center.static_data.static_data import StaticData
from enums import Mode

StaticData.inhabit_class_members()


def load_group(roi, n_subjects, group_index, mode: Mode):
    group_path = config.SUBNET_AVG_N_SUBJECTS.format(mode=mode.value, n_subjects=n_subjects, group_i=group_index)
    roi_path = os.path.join(group_path, f'{roi}.pkl')
    df = pd.read_pickle(roi_path)
    return df


def get_clip_name_by_index(i):
    return StaticData.CLIP_MAPPING.get(str(i))


def get_voxels_per_movie():
    data_clip = load_group(roi='RH_DorsAttn_Post_2', n_subjects=35, group_index=1, mode=Mode.CLIPS)
    data_rest = load_group(roi='RH_DorsAttn_Post_2', n_subjects=35, group_index=1, mode=Mode.REST)
    negative_correlated_movies = ['5', '7', '14']
    flat_correlated_movies = ['8', '11', '3']
    movies = negative_correlated_movies + flat_correlated_movies

    for i in movies:
        movie = get_clip_name_by_index(i)
        clip_window = data_clip[data_clip['y'] == int(i)]
        max_timepoint = clip_window['timepoint'].max()
        end_tr_range = range(max_timepoint - 10, max_timepoint + 1)

        clip_window = clip_window[data_clip['timepoint'].isin(end_tr_range)]
        rest = data_rest[data_rest['y'] == int(i)]

        clip_window = clip_window.drop(['timepoint', 'y'], axis=1).reset_index(drop=True)
        rest = rest.drop(['timepoint', 'y'], axis=1).reset_index(drop=True)

        concat_clip_rest = pd.concat([clip_window, rest], axis=0).reset_index(drop=True)
        concat_clip_rest = z_score(concat_clip_rest, axis=0)
        concat_clip_rest.to_csv(f'RH_DorsAttn_Post_2 voxels {movie.title()}.csv')

        concat_clip_rest.plot(figsize=(16, 8), legend=None)
        plt.title(movie.title(), fontsize=20)
        plt.draw()
        plt.savefig(movie.title() + '.png', dpi=300)
        plt.show()

        print()

        print()

    print()


if __name__ == '__main__':
    get_voxels_per_movie()

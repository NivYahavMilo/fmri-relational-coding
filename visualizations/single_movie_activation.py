import os

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from enums import AnalysisType
from viusalization_utils import gather_dynamic_correlation_by_window


def create_movie_activation_vector(data):
    movie_activation_vectors = {}
    for group, g_values in data.items():
        movie_activation_vectors[group] = {}
        for rest_window, tr_values in g_values.items():
            for movie, value in tr_values.items():
                movie_activation_vectors[group].setdefault(movie, []).append(value)

    movies = [*movie_activation_vectors[1].keys()]
    groups = 6
    rest_windows = 14
    avg_movies = {}
    for movie in movies:
        avg_movies[movie] = {}
        y = np.zeros((groups, rest_windows))
        for group in range(groups):
            y[group, :] = movie_activation_vectors[group + 1][movie]

        avg_movies[movie]['avg'] = y.mean(axis=0)
        avg_movies[movie]['std'] = y.std(axis=0, ddof=1) / np.sqrt(y.shape[0])

    return avg_movies


def plot_single_activation_movie(**kwargs):
    groups_result = gather_dynamic_correlation_by_window(
        n_subjects=35,
        groups=range(1, 7),
        roi='RH_DorsAttn_Post_2',
        init_window='end',
        init_window_start=0,
        init_window_end=5,
        analysis_mode=AnalysisType.SINGLE_MOVIE_ACTIVATION
    )
    averaged_group_results = create_movie_activation_vector(data=groups_result)
    legend = []
    color_names = ['Blue', 'Orange', 'Green', 'Red', 'Purple', 'Brown', 'Pink', 'Gray', 'Yellow', 'Cyan', 'Fuchsia',
                   'Salmon', 'Lime', 'Apricot']

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
              '#17becf', '#a55194', '#ff9896', '#98df8a', '#ffbb78']
    c_i = 0
    for movie, data in averaged_group_results.items():
        std = data['std']
        mean = data['avg']
        sns.set()
        sns.set_theme(style="darkgrid")
        fig = plt.gcf()
        plt.plot(range(0, len(mean)), mean,label=movie, linewidth=4, color=colors[c_i])
        c_i += 1

        plt.fill_between(x=range(0, len(mean)),
                         y1=np.array(mean) + np.array(std),
                         y2=np.array(mean) - np.array(std),
                         facecolor='gray',
                         alpha=0.2)

        legend.append(movie)
    x_ticks = [f'{i}-{j}' for i,j in zip(range(0,14), range(5,19))]
    title = f"Single Movie Activation"
    plt.title(title)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45)
    plt.ylim([-1, .9])
    plt.xlabel('Rest TR window')
    plt.ylabel('Correlation Value')
    plt.legend()

    plt.draw()
    plt.show()
    # if not os.path.isfile(save_fig_path):
    #     fig.savefig(save_fig_path, dpi=300)


if __name__ == '__main__':
    plot_single_activation_movie()

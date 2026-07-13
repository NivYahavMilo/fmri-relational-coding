import pandas as pd


def create_distances_movies_vector(dataframe: pd.DataFrame):
    total_sections = len(dataframe.columns)

    # Split the table into 2 separate clip and rest matrices.
    clips_df = dataframe.iloc[:, 0:total_sections//2]
    rests_df = dataframe.iloc[:, total_sections//2:]
    clips_distances_matrix = _calculate_distance_vectors(clips_df)
    rests_distances_matrix = _calculate_distance_vectors(rests_df)

    dataframe = pd.concat([clips_distances_matrix, rests_distances_matrix], axis=1)
    return dataframe

def _calculate_distance_vectors(dataframe: pd.DataFrame):
    # Calculate the average voxel value for each movie
    movie_averages = dataframe.mean(axis=0)

    # Calculate distance vectors for each movie compared to the rest
    rows = [abs(movie_averages[movie] - movie_averages) for movie in dataframe.columns]
    distance_vectors = pd.DataFrame(rows).reset_index(drop=True)

    return distance_vectors

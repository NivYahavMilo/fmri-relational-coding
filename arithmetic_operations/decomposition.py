from typing import Union

import pandas as pd
from sklearn.decomposition import PCA


class Decomposition:

    @classmethod
    def reduce_dimensions(cls, data: pd.DataFrame, n_components: Union[int,float]):
        X = data.T.values
        # create a PCA object with the desired number of components

        if isinstance(n_components, float):
            n_components = int(n_components * data.shape[1])
        pca = PCA(n_components=n_components)
        # fit the PCA model to the feature data
        pca.fit(X)
        # transform the feature data using the PCA model
        X_pca = pca.transform(X)
        # X_pca now contains the feature data transformed into a lower-dimensional space
        # where each row represents a sample and each column represents a principal component
        X_pca = pd.DataFrame(X_pca.T)
        X_pca.columns = data.columns

        return X_pca

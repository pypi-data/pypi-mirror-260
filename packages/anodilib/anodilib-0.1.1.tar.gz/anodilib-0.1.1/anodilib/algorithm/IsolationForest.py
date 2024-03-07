import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import torch
import pandas as pd

from data.DatasetSpecification import DatasetSpecification


# data
from data.download import *
from data.utils import train_test_split

# isoforest
from sklearn.ensemble import IsolationForest as IF

# utils
from algorithm.utils import *
from data.preprocessing import preprocess, preprocess_with_imputer_and_fixed_normalization_parameters

# Algorithm super-class
from algorithm.algorithm import Algorithm


class IsolationForest(Algorithm):
    def __init__(
        self,
        dataset_specification: DatasetSpecification,
        test_fraction: float = 0.2,
        contamination: float = "auto",
        generator: torch.Generator = None,
        verbose: bool = False
    ):
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)

        if contamination is None:
            contamination = (self.Y_train_df[self.Y_train_df.iloc[:, 0] > 0].shape[0]) / (self.Y_train_df.shape[0])
            if verbose: 
                print('contamination: ', contamination)

        self.contamination = contamination

        self._isoforest = IF(contamination=self.contamination)
        super().__init__(dataset_specification, test_fraction, None, None, generator, verbose)

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        raise Exception("IsolationForests do not need learners")

    def fit(self):
        self._isoforest.fit(self.X_train_df)

    def predict(self, dataset_specification: DatasetSpecification = None):
        if dataset_specification is not None:
            X, Y = get_specification_as_pandas_dataframes(dataset_specification)
            self.X_test_df, self.Y_test_df = preprocess_with_imputer_and_fixed_normalization_parameters(X, Y, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds)

        self.preds = self._isoforest.predict(self.X_test_df)
        return self.preds

    def getAnomalies(self):
        return pd.Series(self.preds).map({1: False, -1: True}).values

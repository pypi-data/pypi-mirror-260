import os
import sys

import numpy as np

from algorithm.algorithm import Algorithm

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from data.DatasetSpecification import DatasetSpecification
from data.download import get_specification_as_pandas_dataframes
from data.utils import train_test_split


class AllTrue(Algorithm):
    def __init__(
            self, dataset_specification: DatasetSpecification, test_fraction: float
    ):
        super().__init__(
            dataset_specification,
            test_fraction,
            learner=None,
            device=None,
            generator=None,
        )
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        _, _, _, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)

    def fit(self, epoch_num: int, learning_rate: float = None):
        pass

    def predict(
            self, dataset_specification: DatasetSpecification = None, with_loss=True
    ):
        if dataset_specification is not None:
            _, self.Y_test_df = get_specification_as_pandas_dataframes(dataset_specification)

    def getAnomalies(self):
        return np.full(len(self.Y_test_df), True)

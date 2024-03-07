import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import torch


# fastai
from fastai.learner import Learner

from data.preprocessing import preprocess

from data.utils import train_test_split

from data.download import *


# pickle
import dill  # can also serialize lambdas, needed for serializing dataset specifications


class Algorithm:
    def __init__(
        self,
        dataset_specification: DatasetSpecification,
        test_fraction: float,
        learner: Learner,
        device: torch.device,
        generator: torch.Generator,
        verbose: bool = False
    ):
        self.dataset_specification = dataset_specification
        self.test_fraction = test_fraction
        self.device = device
        self.learner = learner
        self.generator = generator
        self.verbose = verbose

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        pass

    def fit(self, epoch_num: int, learning_rate: float = None, learning_rate_iteration: int = 50):
        """fits a learner for the given epochnum, learning_rate can be defaulted, set or calculated with 'lr_find'."""
        pass

    def predict(self, dataset_specification: DatasetSpecification = None, with_loss=True):
        """returns tupel of reconstructions and its error if with_loss = True"""
        pass

    def reparseData(self):
        """reparses a training dataset based on the known specification"""
        X_df, Y_df = get_specification_as_pandas_dataframes(self.dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(self.test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)

    def getAnomalies(self):
        """returns (Tensor, Tensor, float) to describe predicted anomalies on time steps"""
        pass

    def updateModelWeights(self, model_path: str, with_opt: bool = True, strict: bool = True,):
        """updates the current weights of the model by overwritting them with those from the given file"""
        self.learner = self.learner.load(model_path, device=self.device, with_opt=with_opt, strict=strict)


def save(
        algorithm: Algorithm,
        model_path: str,
        object_path: str,
        with_opt: bool = True,
        with_data: bool = True
):
    algorithm.learner.save(model_path, with_opt=with_opt, pickle_protocol=2)

    print("Written model")

    generator = algorithm.generator
    algorithm.generator = None
    learner = algorithm.learner
    algorithm.learner = None

    if not with_data:
        X_train_df = algorithm.X_train_df
        algorithm.X_train_df = None
        Y_train_df = algorithm.Y_train_df
        algorithm.Y_train_df = None
        X_test_df = algorithm.X_test_df
        algorithm.X_test_df = None
        Y_test_df = algorithm.Y_test_df
        algorithm.Y_test_df = None
        dropped_columns = algorithm.dropped_columns
        algorithm.dropped_columns = None
        X_train_means = algorithm.X_train_means if hasattr(algorithm, "X_train_means") else None
        algorithm.X_train_means = None
        X_train_stds = algorithm.X_train_stds if hasattr(algorithm, "X_train_stds") else None
        algorithm.X_train_stds = None
        train_dls = algorithm.train_dls
        algorithm.train_dls = None
        test_dls = algorithm.test_dls
        algorithm.test_dls = None

        with open(object_path + ".pickle", "wb") as outfile:
            dill.dump(algorithm, outfile)

        algorithm.X_train_df = X_train_df
        algorithm.Y_train_df = Y_train_df
        algorithm.X_test_df = X_test_df
        algorithm.Y_test_df = Y_test_df
        algorithm.dropped_columns = dropped_columns
        algorithm.X_train_means = X_train_means
        algorithm.X_train_stds = X_train_stds
        algorithm.train_dls = train_dls
        algorithm.test_dls = test_dls
    else:
        with open(object_path + ".pickle", "wb") as outfile:
            dill.dump(algorithm, outfile)

    algorithm.generator = generator
    algorithm.learner = learner
    print("Written object")


def load(
    model_path: str, 
    object_path: str, 
    with_opt: bool = True,
    strict: bool = True,
    device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
) -> Algorithm:    
    with open(object_path, "rb") as infile:
        alg = dill.load(infile)

    print("Loaded Algorithm object")

    if alg.X_train_df is None:
        alg.reparseData()

    tmp_learner = alg.generateEmptyLearner(device)

    alg.learner = tmp_learner.load(model_path, device=device, with_opt=with_opt, strict=strict)

    print("Loaded Learner")

    return alg

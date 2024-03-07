import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import torch
import numpy as np
import pandas as pd


# fastai
from fastai.optimizer import Adam
from fastai.callback.schedule import steep
from model.lstm import ImprovedLSTM as model_lstm

from data.DatasetSpecification import DatasetSpecification

# tsai
from tsai.all import *

# learner
from algorithm.learner import LSTMLearner

# data
from data.download import *
from data.utils import train_test_split

# utils
from algorithm.utils import *
from data.preprocessing import preprocess, preprocess_with_imputer_and_fixed_normalization_parameters

# callbacks
from algorithm.callback import *

# Algorithm super-class
from algorithm.algorithm import Algorithm


class ModifiedLSTM(Algorithm):
    def __init__(
        self,
        dataset_specification: DatasetSpecification,
        test_fraction: float = 0.2,
        hidden_size: int = 25,
        number_layers: int = 1,
        thresh_stepsize: float = 0.01,
        k_max: int = 20,
        clusterselection: int = 0,
        batch_size: int = 64,
        window_len: int = 96,
        stride: int = 1,
        optimizier: torch.optim = Adam,
        learning_rate: float = 1e-3,
        generator: torch.Generator = torch.Generator(device=device),
        device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        verbose: bool = False,
        pruning: bool = False,
        p: float = 0.05,
        t_delta: int = 50
    ):
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)
        self.generator = generator

        self.dim_num = len(self.X_train_df.axes[1])

        self.hidden_size = hidden_size
        self.number_layers = number_layers
        self.thresh_stepsize = thresh_stepsize
        self.k_max = k_max
        self.clusterselection = clusterselection
        self.window_len = window_len
        self.device = device
        self.stride = stride
        self.batch_size = batch_size
        self.optimzier = optimizier
        self.learning_rate = learning_rate
        self.pruning = pruning
        self.p = p
        self.t_delta = t_delta

        _model = model_lstm(
            input_size=self.dim_num,
            hidden_size=hidden_size,
            num_layers=number_layers,
            device=device
        )

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=stride, 
                                                         window_length=window_len,
                                                         batch_size=batch_size,
                                                         device=device)

        class PermutationCallback(Callback):
            def before_batch(self):
                self.learn.xb = (self.xb[0].permute(0, 2, 1),)
                self.learn.yb = self.xb

            def after_pred(self):
                self.learn.pred = self.pred[0]

        self.learner = LSTMLearner(
            self.train_dls,
            model=_model,
            opt_func=self.optimzier,
            loss_func=torch.nn.MSELoss(),
            lr=self.learning_rate,
            cbs=[PermutationCallback()]
        )
        super().__init__(dataset_specification, test_fraction, self.learner, self.device, generator, verbose)

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        model = model_lstm(
            input_size=self.dim_num,
            hidden_size=self.hidden_size,
            num_layers=self.number_layers,
            device=device
        )

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=self.stride, 
                                                         window_length=self.window_len,
                                                         batch_size=self.batch_size,
                                                         device=device)

        class PermutationCallback(Callback):
            def before_batch(self):
                self.learn.xb = (self.xb[0].permute(0, 2, 1),)
                self.learn.yb = self.xb

            def after_pred(self):
                self.learn.pred = self.pred[0]

        learner = LSTMLearner(
            self.train_dls,
            model=model,
            opt_func=self.optimzier,
            loss_func=torch.nn.MSELoss(),
            lr=self.learning_rate,
            cbs=[PermutationCallback()]
        )

        return learner

    def fit(self, epoch_num, learning_rate: float = None, learning_rate_iteration: int = 50):
        self.learner.loss_func = torch.nn.MSELoss()

        if learning_rate is not None:
            if learning_rate == "lr_find":
                learning_rate_iteration = learning_rate_iteration * 2 - 1  # you cant make this shit up (fastAI uses half of the iteration count + 1)
                self.learning_rate = self.learner.lr_find(suggest_funcs=(steep,), num_it=learning_rate_iteration, stop_div=False).steep
            else:
                self.learning_rate = learning_rate

        self.learner.fit(epoch_num, lr=self.learning_rate)

    def predict(self, dataset_specification: DatasetSpecification = None):
        """returns tupel of reconstructions"""
        self.learner.loss_func = torch.nn.MSELoss(reduction="none")

        dl = self.test_dls
        if dataset_specification is not None:
            X, Y = get_specification_as_pandas_dataframes(dataset_specification)
            self.X_test_df, self.Y_test_df = preprocess_with_imputer_and_fixed_normalization_parameters(X, Y, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds)
            _, dl = to_TSDataLoaders(self.X_train_df, 
                                     self.X_test_df,
                                     stride=self.stride,
                                     window_length=self.window_len,
                                     batch_size=self.batch_size,
                                     device=self.device)

        self._preds, self.loss_func_activation, self._pred_errs = self.learner.get_preds(
            ds_idx=0,
            dl=dl.train,
            with_loss=True,
            reorder=False,
            cbs=[LSTMPredCallback()]
        )

        return self._preds, self.loss_func_activation, self._pred_errs

    def getAnomalies(self):
        """returns (Tensor, Tensor, float) to describe predicted anomalies on time steps"""
        _train_preds, train_loss_func_activation, _train_pred_errs = self.learner.get_preds(
            ds_idx=0,
            dl=self.train_dls.train, 
            with_loss=True, 
            reorder=False, 
            cbs=[LSTMPredCallback()]
        )

        # for calculating the threshold
        error_norms = _train_pred_errs.sum(dim=1).tolist()

        # for actual testing
        error_norms_testing = self._pred_errs.sum(dim=1).tolist()

        df_error_norms = pd.DataFrame(error_norms, dtype=float, columns=["Numbers"])
        df_error_norms_testing = pd.DataFrame(error_norms_testing, dtype=float, columns=["Numbers"])

        # input_length=0 because we do not get any values of index < window_size, hence we can use all inputs
        final_anomaly_threshold, optional_lower_threshold = LSTMcalcErrorThreshold(
            df_error_norms, input_length=0, d=self.thresh_stepsize, cluster_selection=self.clusterselection, pruning=self.pruning, verbose=self.verbose, p=self.p, t_delta=self.t_delta
        )

        # concatenate df_error_norms with np zeros of window_size
        df_error_norms_testing = np.array(df_error_norms_testing)[:, 0] 

        if self.verbose:
            print("Anomaly Threshold:", final_anomaly_threshold)

        anomaly_indices = df_error_norms_testing >= final_anomaly_threshold

        anoms = anomaly_indices
        # calculate amounts of the individual _rec_errs vectors, then enter anomalythreshold in calc
        if self.verbose:
            print(f"\n average test_loss: {self._pred_errs.sum().item() / (len(self.X_test_df) * self.window_len * self.dim_num):.4f}")

        return np.concatenate((np.zeros(self.window_len - 1), anoms)), df_error_norms_testing, final_anomaly_threshold

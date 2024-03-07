import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from algorithm.loss import DiffLoss, LogCoshLoss

import torch
import numpy as np


# fastai
from fastai.optimizer import Adam
from fastai.callback.schedule import steep
from model.tcnae import TCNAE as model_tcnae

from data.utils import slide_window_view
from data.DatasetSpecification import DatasetSpecification

# tsai
from tsai.all import *

# learner
from algorithm.learner import TCNAELearner

# data
from data.download import *
from data.utils import train_test_split

# utils
from algorithm.utils import *
from data.preprocessing import preprocess, preprocess_with_imputer_and_fixed_normalization_parameters

# callbacks
from algorithm.callback import *

# Algorithm-superclass
from algorithm.algorithm import Algorithm


class TCNAE(Algorithm):
    def __init__(
        self,
        dataset_specification: DatasetSpecification,
        latent_features: int,  # 4
        kernel_size: int,  # 8
        pool_size: int,  # 32
        dropout: float,  # 0.2
        # TODO: what does this do and can we obtain this from other input parameters?
        num_channels=[32] * 5,
        test_fraction: float = 0.2,
        anomaly_quantile: float = None,
        batch_size: int = 64,
        window_len: int = 96,
        stride: int = 96,
        activation=torch.nn.ReLU,
        learning_rate: float = 1e-3,
        device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        generator: torch.Generator = torch.Generator(device=device),
        verbose: bool = False
    ):
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)

        if anomaly_quantile is None:
            self._anomaly_quantile = 1 - (self.Y_train_df[self.Y_train_df.iloc[:, 0] > 0].shape[0]) / (self.Y_train_df.shape[0])

        self.dim_num = len(self.X_train_df.axes[1])
        self.num_channels = num_channels
        self.latent_features = latent_features
        self.kernel_size = kernel_size
        self.pool_size = pool_size
        self.dropout = dropout
        self.activation = activation
        self.learning_rate = learning_rate

        if verbose:
            print("dim_num", self.dim_num)

        # create model
        self.model = model_tcnae(
            input_features=self.dim_num,
            num_channels=num_channels,
            latent_features=latent_features,
            kernel_size=kernel_size,
            pool_size=pool_size,
            dropout=dropout,
            generator=generator,
            activation=activation,
        )

        self.stride = stride
        self.window_len = window_len
        self.batch_size = batch_size
        self.device = device

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=stride, 
                                                         window_length=window_len,
                                                         batch_size=batch_size,
                                                         device=device)

        # create learner object
        self.learner = TCNAELearner(
            dls=self.train_dls,
            model=self.model,
            opt_func=Adam,
            loss_func=LogCoshLoss(),
            lr=learning_rate,
        )
        super().__init__(dataset_specification, test_fraction, self.learner, self.device, generator, verbose)

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        model = model_tcnae(
            input_features=self.dim_num,
            num_channels=self.num_channels,
            latent_features=self.latent_features,
            kernel_size=self.kernel_size,
            pool_size=self.pool_size,
            dropout=self.dropout,
            generator=self.generator,
            activation=self.activation,
        )

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=self.stride, 
                                                         window_length=self.window_len,
                                                         batch_size=self.batch_size,
                                                         device=device)

        # create learner object
        learner = TCNAELearner(
            dls=self.train_dls,
            model=model,
            opt_func=Adam,
            loss_func=LogCoshLoss(),
            lr=self.learning_rate,
        )

        return learner

    def fit(self, epoch_num: int, learning_rate: float = None, learning_rate_iteration: int = 50):
        """fits the learner on the number of epochs"""
        # reset Loss Function
        self.learner.loss_func = LogCoshLoss()

        if learning_rate is not None:
            if learning_rate == "lr_find":
                learning_rate_iteration = learning_rate_iteration * 2 - 1  # you cant make this shit up (fastAI uses half of the iteration count + 1)
                self.learning_rate = self.learner.lr_find(suggest_funcs=(steep,), num_it=learning_rate_iteration, stop_div=False).steep
            else:
                self.learning_rate = learning_rate

        self.learner.fit(epoch_num, lr=self.learning_rate)

    def predict(self, dataset_specification: DatasetSpecification = None, with_loss=True, reorder=False):
        """returns tupel of reconstructions and its error if with_loss = True"""
        # define new loss function for prediction
        loss_func_pred = lambda x, y, reduction=None: DiffLoss()(x, y)
        self.learner.loss_func = loss_func_pred

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

        self._recs, self._loss_func_activation, self._rec_errs = self.learner.get_preds(
            ds_idx=0, dl=dl.train, with_loss=True, reorder=reorder
        )
        return (self._recs, self._rec_errs) if with_loss else (self._recs,)

    # TODO: what do these 2 parameters actually do
    def getAnomalies(self, rec_errs=None, error_window_len=12, smooth_window_len=5):
        """returns (Tensor, Tensor, float) to describe predicted anomalies on time steps"""
        if rec_errs is None:
            rec_errs = self._rec_errs
        _errs = slide_window_view(rec_errs.detach().numpy(), error_window_len, stride=1)
        _errs = _errs.reshape(-1, _errs.shape[-1] * _errs.shape[-2])
        _sel_num = np.floor(_errs.shape[0] * 0.98).astype(np.intc)
        sel = (
            # TODO Here smth has to be also moved to MPS Device for ARM64 Architecture
            torch.empty((_sel_num), dtype=torch.int)
            .random_(to=_errs.shape[0], generator=self.generator)
            .numpy()
        )
        mu = np.mean(_errs[sel], axis=0)
        cov = np.cov(_errs[sel], rowvar=False)
        sq_mahalanobis = mahalanobis_distance(X=_errs[:], cov=cov, mu=mu)
        # moving average over mahalanobis distance. Only slightly smooths the signal

        if smooth_window_len > 0:
            anomaly_score = np.convolve(
                sq_mahalanobis,
                np.ones((smooth_window_len,)) / smooth_window_len,
                mode="same",
            )
        anomaly_score = np.sqrt(anomaly_score)

        # _feat_errs are the anomaly scores
        _feat_errs = rec_errs[:, :-2, :].mean(dim=(1, 2))
        # Parameter set by user by default
        _thresh = _feat_errs.quantile(self._anomaly_quantile)
        # preds are the anomalies
        _ano_preds = _feat_errs > _thresh
        return _ano_preds, _feat_errs, _thresh

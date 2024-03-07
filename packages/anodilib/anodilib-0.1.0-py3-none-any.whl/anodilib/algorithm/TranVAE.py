import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import torch
import numpy as np


# fastai
from fastai.optimizer import Adam
from fastai.callback.schedule import steep
from model.tranvae import TranVAE as model_tranvae

from data.DatasetSpecification import DatasetSpecification

# tsai
from tsai.all import *

# learner
from algorithm.learner import TranVAELearner

# data
from data.download import *
from data.utils import train_test_split

# utils
from algorithm.utils import *
from data.preprocessing import preprocess, preprocess_with_imputer_and_fixed_normalization_parameters

# loss
from algorithm.loss import ELBOLoss

# callbacks
from algorithm.callback import *

# Algorithm super-class
from algorithm.algorithm import Algorithm


class TranVAE(Algorithm):
    def __init__(
            self, 
            dataset_specification: DatasetSpecification,
            num_layers: int,
            test_fraction: float = 0.2,
            out_dim: int = None, 
            batch_size: int = 64,
            learning_rate: float = 0.001,
            window_length: int = 96,
            # stride: int = 96, must not be set in TranVAE
            q: float = 0.001,  # both q and level kinda random picked from mtad gat repo
            level: float = 0.98,
            reg_level=1,  # can be different per dataset
            dynamic_pot: bool = False,
            n_z: int = 10,
            kld_weight: float = 0.5,
            generator: torch.Generator = torch.Generator(device=device),
            device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            verbose: bool = False
    ):
        self.test_fraction = test_fraction
        self.num_layers = num_layers
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.window_length = window_length
        self.stride = window_length
        self.dynamic_pot = dynamic_pot
        self.q = q
        self.level = level
        self.reg_level = reg_level
        self.n_z = n_z
        self.kld_weight = kld_weight
        self.generator = generator
        self.device = device

        # impute and normalize the data columns
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)

        self.dim_num = len(self.X_train_df.axes[1])

        self.out_dim = out_dim
        if self.out_dim is None:
            self.out_dim = self.dim_num

        self.model = model_tranvae(input_dim=self.dim_num,
                                   num_layers=self.num_layers,
                                   device=self.device,
                                   n_z=self.n_z)

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         Y_train=self.Y_train_df,
                                                         Y_test=self.Y_test_df,
                                                         stride=self.stride, 
                                                         window_length=self.window_length,
                                                         batch_size=batch_size,
                                                         device=device)

        self.learner = TranVAELearner(
            dls=self.train_dls,
            model=self.model,
            opt_func=Adam,
            lr=learning_rate,
            loss_func=ELBOLoss(kld_weight=kld_weight),
            cbs=[SwapSequenceChannelCallbackTranVae()],
        )

        self._scores_training = None
        self._scores_test = None
        self._labels_test = None
        super().__init__(dataset_specification, test_fraction, self.learner, self.device, generator, verbose)

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        model = model_tranvae(input_dim=self.dim_num,
                              num_layers=self.num_layers,
                              device=device,
                              n_z=self.n_z)

        class SwapSequenceChannelCallback(Callback):
            def before_batch(self):
                self.learn.xb = (self.xb[0].permute(0, 2, 1),)

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         Y_train=self.Y_train_df,
                                                         Y_test=self.Y_test_df,
                                                         stride=self.stride, 
                                                         window_length=self.window_length,
                                                         batch_size=self.batch_size,
                                                         device=device)

        learner = TranVAELearner(
            dls=self.train_dls,
            model=model,
            opt_func=Adam,
            lr=self.learning_rate,
            loss_func=ELBOLoss(kld_weight=self.kld_weight),
            cbs=[SwapSequenceChannelCallback()],
        )

        return learner

    def fit(self, epoch_num: int, learning_rate: float = None, learning_rate_iteration: int = 50):
        """fits the learner on the number of epochs"""
        # reset Loss Function
        if learning_rate is not None:
            if learning_rate == "lr_find":
                learning_rate_iteration = learning_rate_iteration * 2 - 1  # you cant make this shit up (fastAI uses half of the iteration count + 1)
                self.learning_rate = self.learner.lr_find(suggest_funcs=(steep,), num_it=learning_rate_iteration, stop_div=False).steep
            else:
                self.learning_rate = learning_rate

        self.learner.fit(epoch_num, lr=self.learning_rate)

    def predict(self, dataset_specification: DatasetSpecification = None):
        """returns tupel of reconstructions and its error if with_loss = True"""   
        # Not giving with_loss here since it is not clear if the user needs and MSELoss for reconstruction or the training ELBOLoss 
        dl = self.test_dls
        if dataset_specification is not None:
            X, Y = get_specification_as_pandas_dataframes(dataset_specification)
            self.X_test_df, self.Y_test_df = preprocess_with_imputer_and_fixed_normalization_parameters(X, Y, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds)
            _, dl = to_TSDataLoaders(self.X_train_df, 
                                     self.X_test_df,
                                     stride=self.stride,
                                     window_length=self.window_length,
                                     batch_size=self.batch_size,
                                     device=self.device)

        if self._scores_training is None:
            scores_training, _ = self.learner.get_preds(ds_idx=0, dl=self.train_dls.train, reorder=False)
            self._scores_training = torch.flatten(scores_training).detach().numpy()

        scores_test, _ = self.learner.get_preds(ds_idx=0, dl=dl.train, reorder=False)
        self._scores_test = torch.flatten(scores_test).detach().numpy()
        # No idea how to get labels directly from the data loader
        self._labels_test = np.array(self.Y_test_df[:len(self._scores_test)]).squeeze()

        return self._scores_test

    def getAnomalies(self):
        """returns (Tensor, Tensor, float) to describe predicted anomalies on time steps"""
        if self._scores_training is None or self._scores_test is None or self._labels_test is None:
            raise NotImplementedError()
        train_anomaly_scores = self._scores_training
        test_anomaly_scores = self._scores_test
        true_anomalies = self._labels_test
        e_eval, e_eval_preds = epsilon_eval(train_anomaly_scores, test_anomaly_scores, true_anomalies, reg_level=self.reg_level)
        p_eval = pot_eval(init_score=train_anomaly_scores,
                          score=test_anomaly_scores, 
                          label=true_anomalies,
                          q=self.q, 
                          level=self.level, 
                          dynamic=self.dynamic_pot,
                          min_extrema=False,
                          verbose=self.verbose)
        if true_anomalies is not None:
            bf_eval = bf_search(test_anomaly_scores, true_anomalies, start=0.01, end=2, step_num=100, verbose=self.verbose)
        else:
            bf_eval = {}

        if self.verbose:
            print(f"Results using epsilon method:\n {e_eval}")
            print(f"Results using peak-over-threshold method:\n {p_eval}")
            print(f"Results using best f1 score search:\n {bf_eval}")

        for k, v in e_eval.items():
            if not isinstance(e_eval[k], list):
                e_eval[k] = float(v)
        for k, v in p_eval.items():
            if not isinstance(p_eval[k], list):
                p_eval[k] = float(v)
        for k, v in bf_eval.items():
            bf_eval[k] = float(v)

        # own anomaly calc
        eps = p_eval["threshold"]
        test_anom_labls = test_anomaly_scores >= eps
        # train_anom_labls = train_anomaly_scores >= eps

        bf_preds = test_anomaly_scores >= bf_eval["threshold"]

        missing_window_len = self.Y_test_df.shape[0] - len(bf_preds)
        # Some datasets (WADI) have DataLoaders with more values to predict than labels, 
        # leading to a negative missing_window_len padding
        if missing_window_len > 0: 
            filler_array = np.zeros(missing_window_len)
            test_anom_labls = np.concatenate((test_anom_labls, filler_array))
            e_eval_preds = np.concatenate((e_eval_preds, filler_array))
            bf_preds = np.concatenate((bf_preds, filler_array))
        return (test_anom_labls, e_eval_preds, bf_preds), test_anomaly_scores, (e_eval["threshold"], p_eval["threshold"], bf_eval["threshold"])

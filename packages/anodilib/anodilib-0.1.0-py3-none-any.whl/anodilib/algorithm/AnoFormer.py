import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import torch
import numpy as np
import pandas as pd


# fastai
from fastai.learner import Learner
from fastai.optimizer import Adam
from fastai.callback.schedule import steep
from model.ano_former import AnoFormer as model_ano_former

from data.DatasetSpecification import DatasetSpecification

# tsai
from tsai.all import *

# data
from data.download import *
from data.utils import train_test_split

# utils
from algorithm.utils import *
from data.preprocessing import preprocess_anoformer, preprocess_with_imputer_and_fixed_normalization_parameters_anoformer

# callbacks
from algorithm.callback import *

# Algorithm super-class
from algorithm.algorithm import Algorithm

class AnoFormer(Algorithm):
    def __init__(
            self,
            dataset_specification: DatasetSpecification,
            test_fraction: float = 0.2,
            optimizer: torch.optim = Adam,
            learning_rate: float = 1e-4,
            generator: torch.Generator = torch.Generator(device=device),
            device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            verbose: bool = False,
            batch_size: int = 64,
            window_len: int = 96,
            stride: int = 1,
            n_critic: int = 0, #5, but generator-only
            K: int = 200,
            d: int = 40,
            dim_feedforward: int = 200,
            substitute_value: callable = lambda x : 0,
            critic_opt: torch.optim = torch.optim.Adam,
            Llambda: float = 10,
            lambda_rec: float = 1,  # weighting of losses of generator
            lambda_adv: float = 0, #1, but mse-loss only  # weighting of losses of generator
            anomaly_quantile: float = None,
            L: int = 9, #not a magic number anymore, found it in paper
            critic_L: int = 0, #6, but generator-only
    ):
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_min, self.X_max = preprocess_anoformer(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, K)
        self.generator = generator

        self._anomaly_quantile = anomaly_quantile
        if anomaly_quantile is None:
            self._anomaly_quantile = 1 - (self.Y_train_df[self.Y_train_df.iloc[:, 0] > 0].shape[0]) / (self.Y_train_df.shape[0])

        self.dim_num = len(self.X_train_df.axes[1])

        self.window_len = window_len
        self.device = device
        self.stride = stride
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.n_critic = n_critic
        self.K = K
        self.d = d
        self.substitute_value = substitute_value
        self.lambda_adv = lambda_adv
        self.lambda_rec = lambda_rec
        self.Llambda = Llambda
        self.L = L
        self.critic_L = critic_L
        self.dim_feedforward = dim_feedforward
        self.verbose = verbose

        if critic_L == 0 or n_critic == 0: # safety to not call critic without transformer-stack or to not initialize a big transformer stack for no critic
            self.critic_L, self.n_critic = 0, 0

        self.critic_opt = critic_opt
        self.critic_lr = learning_rate

        if self.stride != 1:
            raise NotImplementedError("stride must be 1")

        self.model = model_ano_former(
            n_critic=n_critic,
            input_length=window_len,
            d=self.d,
            K=K,
            dim_num=self.dim_num,
            substitute_value=substitute_value,
            critic_opt=self.critic_opt,
            critic_lr=self.critic_lr,
            critic_L=self.critic_L,
            dim_feedforward=dim_feedforward,
            Llambda=Llambda,
            L=self.L,
            verbose=self.verbose
        )

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=stride, 
                                                         window_length=window_len,
                                                         batch_size=batch_size,
                                                         device=device)
        
        def generator_trainable_params(m):
            "Only params of Generator"
            return [p for p in m.generator.parameters() if p.requires_grad]

        self.learner = Learner(
            self.train_dls,
            model=self.model,
            opt_func=self.optimizer,
            loss_func=self.loss,
            lr=self.learning_rate,
            cbs=[SwapSequenceChannelCallbackAnoFormer()],
            splitter=generator_trainable_params
        )

        super().__init__(dataset_specification, test_fraction, self.learner, self.device, generator, verbose)

    def reparseData(self):
        X_df, Y_df = get_specification_as_pandas_dataframes(self.dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(self.test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_min, self.X_max = preprocess_anoformer(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.K)

    def loss(self, x, y):
        # self.model.critic_train_count = 0
        generator_out, fake_data = x
        return self.lambda_rec * self.model.L_g_rec(generator_out, y) + self.lambda_adv * self.model.L_g_adv(fake_data)

    def fit(self, epoch_num, learning_rate: float = None, learning_rate_iteration: int = 50):
        self.learner.loss_func = self.loss
        self.learner.model.train_phase = True
        if learning_rate is not None:
            if learning_rate == "lr_find":
                learning_rate_iteration = learning_rate_iteration * 2 - 1  # you cant make this shit up (fastAI uses half of the iteration count + 1)
                self.learning_rate = self.learner.lr_find(suggest_funcs=(steep,), num_it=learning_rate_iteration, stop_div=False).steep
            else:
                self.learning_rate = learning_rate

        self.learner.fit(epoch_num, lr=self.learning_rate)

    def predict(self, dataset_specification: DatasetSpecification = None):

        self.learner.model.train_phase = False

        dl = self.test_dls
        if dataset_specification is not None:
            X, Y = get_specification_as_pandas_dataframes(dataset_specification)
            self.X_test_df, self.Y_test_df = preprocess_with_imputer_and_fixed_normalization_parameters_anoformer(X, Y, self.imputer, self.dropped_columns, self.X_min, self.X_max, self.K)
            _, dl = to_TSDataLoaders(self.X_train_df, 
                                     self.X_test_df,
                                     stride=self.stride,
                                     window_length=self.window_len,
                                     batch_size=self.batch_size,
                                     device=self.device)
            
        self.learner.loss_func = torch.nn.MSELoss(reduction="None")

        not_reduced_errors = []
        class PredCallback(Callback):
            def after_loss(self):
                not_reduced_errors.append(self.loss.mean(dim=2))
                self.learn.loss = self.loss.mean(dim=(1,2))

        self._preds, self.loss_func_activation, self._pred_errs = self.learner.get_preds(
            ds_idx=0,
            dl=dl.train,
            with_loss=True,
            reorder=False,
            cbs=[PredCallback()]
        )


        if self.stride == 1: self.test_pred_errs = torch.cat(not_reduced_errors, dim=0).mean(dim=1)
        elif self.stride == self.window_len: self.test_pred_errs = torch.cat(not_reduced_errors, dim=0).flatten()
        else:
            print("Stride must be either 1 or window length")
            return

        not_reduced_errors = []

        self._preds, self.loss_func_activation, self._pred_errs = self.learner.get_preds(
            ds_idx=0,
            dl=self.train_dls.train,
            with_loss=True,
            reorder=False,
            cbs=[PredCallback()]
        )

        if self.stride == 1: self.train_pred_errs = torch.cat(not_reduced_errors, dim=0).mean(dim=1)
        elif self.stride == self.window_len: self.train_pred_errs = torch.cat(not_reduced_errors, dim=0).flatten() 
        else:
            print("Stride must be either 1 or window length")
            return

        return self._preds, self.loss_func_activation, self.train_pred_errs, self.test_pred_errs


    def getAnomalies(self, train_pred_errs: torch.Tensor = None, test_pred_errs: torch.Tensor = None, quantile: float = None):
        """returns (Tensor, float)"""

        if train_pred_errs is not None:
            self.train_pred_errs = train_pred_errs
        if test_pred_errs is not None:
            self.test_pred_errs = test_pred_errs
        
        if quantile is None:
            quantile = self._anomaly_quantile
            
        quantile = quantile - torch.floor(torch.Tensor([quantile])).item()

        train_len = len(self.train_pred_errs)
        sorted_train = torch.sort(self.train_pred_errs)[0]
        threshold = sorted_train[int(quantile * train_len)]

        anomaly_preds = self.test_pred_errs > threshold
        anomaly_preds = anomaly_preds.detach().cpu().numpy()

        # add window length - 1 zeros at the end, cause slide_window_view cuts at that entry
        anomaly_preds = np.concatenate((anomaly_preds, (np.zeros(self.window_len - 1))))

        return anomaly_preds, threshold



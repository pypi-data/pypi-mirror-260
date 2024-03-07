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
from model.mtad_gat import MTAD_GAT as model_mtad_gat

from data.DatasetSpecification import DatasetSpecification

# tsai
from tsai.all import *

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


class MTAD_GAT(Algorithm):
    """
        MTAD-GAT-Model from https://ieeexplore.ieee.org/abstract/document/9338317?casa_token=ruOmRmqBOWQAAAAA:bfElVB9cwDOuKUYA20saxZoPzmeoakyMguKxsxWlZjjsJNOHuIEEOTve5DWb5rIKSMKHcVc4
        stride has to be same as window_length, because every time stamp is represented by the window, so if stride > 1 there are holey timeseries'

        Note on the score calculation:
        The forecaster implicitly predicts (the window length is increased by 1 just to get the value) the last value 
        of the next window (for stride=1 this is the window_length+1_th value) and
        the reconstructer outputs scores for the last value of the current window.
        The scores are representative of the first window_length values of the window_length+1-long window.
        The first window_length-1 values cannot be scored.
        And because the last value of the time series is the window_length+1_th value of the last window,
        which is needed for the forecaster score, this timestamp cannot be scored either.
        """
    def __init__(
            self, 
            dataset_specification: DatasetSpecification,
            test_fraction: float = 0.2,
            batch_size: int = 64, 
            out_dim: int = None,
            learning_rate: float = 0.001,
            window_length: int = 96,
            L: int = 10,
            use_move_avg=True,
            q: float = 0.001,  # both q and level kinda random picked from mtad gat repo
            level: float = 0.8,  # quantile to get the initial threshold for pot_eval #former 0.02 cause min_extrema change from True to False in old github-code in utils.pot_eval
            min_extrema: bool = False,  # former False cause min_extrema change from True to False in old github-code in utils.pot_eval
            reg_level=1,  # can be different per dataset
            dynamic_pot=False,
            gamma=0.01,
            recon_latent_dim=50,
            optimizier: torch.optim = Adam,
            generator: torch.Generator = torch.Generator(device=device),
            device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            verbose: bool = False
    ):
        """
        @param L: sample size for monte carlo sampling in inference
        @params q, level, min_extrema, reg_level: for pot evaluation
        @param gamma: tradeoff between forecast- and reconprob-anomaly-score
        """
        self.test_fraction = test_fraction
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.window_length = window_length
        self.stride = 1  # see doc
        self.L = L
        self.use_move_avg = use_move_avg
        self.q = q
        self.level = level
        self.min_extrema = min_extrema
        self.reg_level = reg_level
        self.dynamic_pot = dynamic_pot
        self.gamma = gamma
        self.recon_latent_dim = recon_latent_dim
        self.generator = generator
        self.device = device
        self.optimizier = optimizier    

        # impute and normalize the data columns
        X_df, Y_df = get_specification_as_pandas_dataframes(dataset_specification)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df = train_test_split(test_fraction, True, X_df, Y_df)
        self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds = preprocess(self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df)

        self.dim_num = len(self.X_train_df.axes[1])

        self.out_dim = out_dim
        if self.out_dim is None:
            self.out_dim = self.dim_num

        self.model = model_mtad_gat(self.dim_num, self.window_length, self.out_dim, recon_latent_dim=self.recon_latent_dim, L=self.L)

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=self.stride, 
                                                         window_length=self.window_length + 1,  # damit fürs forcasting der letzte Wert vom nächsten Fenster
                                                         batch_size=batch_size,
                                                         device=device)

        self.learner = Learner(self.train_dls, self.model, opt_func=optimizier, lr=self.learning_rate, loss_func=self._criterion, cbs=[MTAD_GATFitCallback()])
        super().__init__(dataset_specification, test_fraction, self.learner, self.device, generator, verbose)

    @staticmethod
    def _criterion(x, y):
        """
        sets forecast- and reconstruction-loss together
        """

        forecast_criterion = torch.nn.MSELoss(reduction="mean")

        preds, recons, (enll, kl_div) = x

        if preds.ndim == 3:
            preds = preds.squeeze(1)
        if y.ndim == 3:
            y = y.squeeze(1)

        recon_loss = enll + kl_div

        # compare forecasted with "next" 
        forecast_loss = torch.sqrt(forecast_criterion(y, preds))
        _train_loss = forecast_loss + recon_loss.mean(dim=0)

        return _train_loss  

    def generateEmptyLearner(self, device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        """returns a new Learner object that fits the algorithm structure. This is needed for deserialization."""
        forecast_criterion = torch.nn.MSELoss(reduction="mean")    

        model = model_mtad_gat(self.dim_num, self.window_length, self.out_dim)

        self.train_dls, self.test_dls = to_TSDataLoaders(X_train=self.X_train_df, 
                                                         X_test=self.X_test_df, 
                                                         stride=self.stride, 
                                                         window_length=self.window_length + 1,  # damit fürs forcasting der letzte Wert vom nächsten Fenster
                                                         batch_size=self.batch_size,
                                                         device=device)

        learner = Learner(self.train_dls, model, opt_func=self.optimizier, lr=self.learning_rate, loss_func=self._criterion, cbs=[MTAD_GATFitCallback()])

        return learner

    def fit(self, epoch_num, learning_rate: float = None, learning_rate_iteration: int = 50):

        self.learner.loss_func = self._criterion

        self.learner.model.recon_model.inference = False

        if learning_rate is not None:
            if learning_rate == "lr_find":
                learning_rate_iteration = learning_rate_iteration * 2 - 1  # you cant make this shit up (fastAI uses half of the iteration count + 1)
                self.learning_rate = self.learner.lr_find(suggest_funcs=(steep,), num_it=learning_rate_iteration, stop_div=False).steep
            else:
                self.learning_rate = learning_rate

        self.learner.fit(epoch_num, lr=self.learning_rate)

    def predict(self, dataset_specification: DatasetSpecification = None):
        """returns tupel of reconstructions"""
        dl = self.test_dls
        if dataset_specification is not None:
            X, Y = get_specification_as_pandas_dataframes(dataset_specification)
            self.X_test_df, self.Y_test_df = preprocess_with_imputer_and_fixed_normalization_parameters(X, Y, self.imputer, self.dropped_columns, self.X_train_means, self.X_train_stds)
            _, dl = to_TSDataLoaders(self.X_train_df, 
                                     self.X_test_df,
                                     stride=self.stride,
                                     window_length=self.window_length + 1,  # last value from next window for forecasting
                                     batch_size=self.batch_size,
                                     device=self.device)

        def inner_predict(learner, test_dls, device, gamma):
            """
            gets model-outputs for all data
            """

            learner.loss_func = lambda x, y, reduction="None": torch.zeros(x[0].shape[0]).to(device)
            learner.model.recon_model.inference = True
            preds = []
            recons = []
            values = []

            class PredCallback(Callback):
                def after_pred(self):
                    y_hat, window_recon, recon_prob = self.pred
                    _next = self.yb[0]

                    preds.append(y_hat.detach().cpu().numpy())
                    # Extract last reconstruction only
                    recons.append(recon_prob.detach().cpu().numpy())
                    values.append(_next.clone().detach().cpu().numpy())  # to get original predicted values as tensors

                def after_loss(self):
                    self.learn.pred = self.pred[2]  # for GatherPredsCallback to work

            _preds, loss_func_activation, _pred_errs = learner.get_preds(ds_idx=0, dl=test_dls.train, with_loss=True, reorder=False, cbs=[PredCallback()])

            preds = np.concatenate(preds, axis=0)
            recons = np.concatenate(recons, axis=0)
            values = np.concatenate(values, axis=0)
            actual = values  # for prediction, the first window is never predicted so we dont need it; can also be done by taking all data and slice it accordingly

            anomaly_scores = np.zeros_like(actual)
            df_dict = {}
            for i in range(preds.shape[1]):
                df_dict[f"Forecast_{i}"] = preds[:, i]
                df_dict[f"Recon_{i}"] = recons[:, i]
                df_dict[f"True_{i}"] = actual[:, i]

                a_score = ((preds[:, i] - actual[:, i])**2 + gamma * (1 - recons[:, i])) / (1 + gamma)

                anomaly_scores[:, i] = a_score
                df_dict[f"A_Score_{i}"] = a_score

            df = pd.DataFrame(df_dict)
            anomaly_scores = np.sum(anomaly_scores, axis=1)  # was mean in github code
            df['A_Score_Global'] = anomaly_scores
            df['A_Forecast_Global'] = np.sum(preds, axis=1)
            df['A_Recon_Global'] = np.sum(recons, axis=1)

            return df, (preds, recons, learner.yb[0])

        # fastai-get_preds is to low level for our predict-method, so we put it in as a part of our predict
        self.train_pred_df, self.preds_train = inner_predict(self.learner, self.train_dls, self.device, gamma=self.gamma) 
        self.test_pred_df, self.preds_test = inner_predict(self.learner, dl, self.device, gamma=self.gamma)

        return self.train_pred_df, self.preds_train, self.test_pred_df, self.preds_test

    def getAnomalies(self, train_pred_df: pd.DataFrame = None, test_pred_df: pd.DataFrame = None):
        """returns (Tensor, Tensor, float) to describe predicted anomalies on time steps"""

        if train_pred_df is not None:
            self.train_pred_df = train_pred_df
        if test_pred_df is not None:
            self.test_pred_df = test_pred_df

        true_anomalies = np.array(self.Y_test_df)
        if len(true_anomalies.shape) != 1:
            true_anomalies = true_anomalies[:, 0]

        train_anomaly_scores = self.train_pred_df['A_Score_Global'].values
        test_anomaly_scores = self.test_pred_df['A_Score_Global'].values

        # Update df
        self.train_pred_df['A_Score_Global'] = train_anomaly_scores
        self.test_pred_df['A_Score_Global'] = test_anomaly_scores

        if self.use_move_avg:
            smoothing_window = int(self.batch_size * self.window_length * 0.05)
            train_anomaly_scores = pd.DataFrame(train_anomaly_scores).ewm(span=smoothing_window).mean().values.flatten()
            test_anomaly_scores = pd.DataFrame(test_anomaly_scores).ewm(span=smoothing_window).mean().values.flatten()

        # be found unuseful, could be removed

        # Find threshold and predict anomalies at feature-level (for plotting and diagnosis purposes)
        # all_preds = np.zeros((len(self.test_pred_df), self.out_dim))
        # for i in range(self.out_dim):
        #     train_feature_anom_scores = self.train_pred_df[f"A_Score_{i}"].values
        #     test_feature_anom_scores = self.test_pred_df[f"A_Score_{i}"].values
        #     epsilon = find_epsilon(train_feature_anom_scores, reg_level=2)

        #     train_feature_anom_preds = (train_feature_anom_scores >= epsilon).astype(int)
        #     test_feature_anom_preds = (test_feature_anom_scores >= epsilon).astype(int)

        #     self.train_pred_df[f"A_Pred_{i}"] = train_feature_anom_preds
        #     self.test_pred_df[f"A_Pred_{i}"] = test_feature_anom_preds

        #     self.train_pred_df[f"Thresh_{i}"] = epsilon
        #     self.test_pred_df[f"Thresh_{i}"] = epsilon

        #     all_preds[:, i] = test_feature_anom_preds

        test_anomaly_scores = np.concatenate((np.zeros(self.window_length - 1), test_anomaly_scores, np.zeros(1)))
        train_anomaly_scores = np.concatenate((np.zeros(self.window_length - 1), train_anomaly_scores, np.zeros(1)))

        # Global anomalies (entity-level) are predicted using aggregation of anomaly scores across all features
        # These predictions are used to evaluate performance, as true anomalies are labeled at entity-level
        # Evaluate using different threshold methods: brute-force, epsilon and peaks-over-treshold
        e_eval, e_eval_preds = epsilon_eval(train_anomaly_scores, test_anomaly_scores, true_anomalies, reg_level=self.reg_level)
        p_eval = pot_eval(train_anomaly_scores, test_anomaly_scores, true_anomalies, q=self.q, level=self.level, 
                          dynamic=self.dynamic_pot, min_extrema=self.min_extrema, verbose=self.verbose)
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
        test_anom_labels = test_anomaly_scores >= eps

        bf_preds = test_anomaly_scores >= bf_eval["threshold"]

        return (test_anom_labels, e_eval_preds, bf_preds), test_anomaly_scores, (e_eval["threshold"], p_eval["threshold"], bf_eval["threshold"])

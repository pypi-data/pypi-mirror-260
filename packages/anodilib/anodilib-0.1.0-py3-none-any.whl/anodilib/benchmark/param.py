import os
import sys
from typing import Callable

import numpy as np

from modelWrapper import EpochRange, ModelWrapper
from paramSet import AnoFormerParams, EmptyParams, MLSTMParams, MTAD_GATParams, RandomParams, TranVAEParams

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.AnoFormer import AnoFormer
from algorithm.IsolationForest import IsolationForest
from algorithm.ModifiedLSTM import ModifiedLSTM
from algorithm.MTAD_GAT import MTAD_GAT
from algorithm.TranVAE import TranVAE
from algorithm.Random import Random
from algorithm.AllFalse import AllFalse
from algorithm.AllTrue import AllTrue
from algorithm.NPRandom import NPRandom
from data.DatasetSpecification import DatasetSpecification, EF42_TEST_SYN_V2_18, EF42_TRAIN, IOT23_SMALL_LABELED, IOT23_SMALL_LABELED_2, SWAT, WADI, \
    WAFER_TRAIN, WAFER_TEST

PS_DEFAULT_EPOCH_RANGE = EpochRange(50, 1)
SINGLE_EPOCH_RANGE = EpochRange(1, 1)

PS_RAW_FILE: str = "anodi/benchmark/files/ps_raw.pkl"
BM_RAW_FILE: str = "anodi/benchmark/files/bm_raw.pkl"
PS_SCORES_FILE: str = "anodi/benchmark/files/ps_scores.pkl"
BM_SCORES_FILE: str = "anodi/benchmark/files/bm_scores.pkl"
BEST_PARAMS_FILE: str = "anodi/benchmark/files/best_params.csv"

datasets: dict[str, list[DatasetSpecification]] = {
    "EF42": [EF42_TRAIN, EF42_TEST_SYN_V2_18],
    "IOT23": [IOT23_SMALL_LABELED],
    "IOT23-2": [IOT23_SMALL_LABELED_2],
    "SWAT": [SWAT],
    "WADI": [WADI],
    "WAFER": [WAFER_TRAIN, WAFER_TEST]
}


def window_size(datasetId: str):
    if datasetId == "EF42":
        return 96
    else:
        return 100


def applyAnoFormerAnomalyParams(alg: AnoFormer, paramSet: AnoFormerParams):
    alg._anomaly_quantile = paramSet.anomaly_quantile


def applyMLSTMAnomalyParams(alg: ModifiedLSTM, paramSet: MLSTMParams):
    alg.thresh_stepsize = paramSet.thresh_stepsize
    alg.clusterselection = paramSet.clusterselection
    alg.pruning = paramSet.pruning
    alg.p = paramSet.p
    alg.t_delta = paramSet.t_delta


def applyRandomAnomalyParams(alg: Random, paramSet: RandomParams):
    alg.p_anom = paramSet.p_anom


def getAFSubstituteValueFuncs(K: int) -> list[Callable]:
    lambdas = [lambda x: 0, lambda x: 0.5 * K, lambda x: K - 1, lambda x: x.mean(dim=(0, 1))[None, None, :]]
    lambdas[0].__name__ = "0"
    lambdas[1].__name__ = "0.5*K"
    lambdas[2].__name__ = "K-1"
    lambdas[3].__name__ = "x.mean(dim=(0, 1))[None, None, :]]"
    return lambdas


def getAnoFormerPSParams(datasetId: str) -> list[list[AnoFormerParams]]:
    if datasetId == "EF42":
        return ([[AnoFormerParams(K, 100, dim_feedforward, substitute_value, anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for K in [100, 200]
                 for dim_feedforward in [400, 900]
                 for substitute_value in getAFSubstituteValueFuncs(K)
                 for L in [4, 9]] +
                [[AnoFormerParams(200, 100, 400, getAFSubstituteValueFuncs(200)[3], anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for L in [2, 6]])
    elif datasetId == "IOT23":
        return ([[AnoFormerParams(K, 100, dim_feedforward, substitute_value, anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for K in [100, 200]
                 for dim_feedforward in [400, 900]
                 for substitute_value in getAFSubstituteValueFuncs(K)
                 for L in [4, 9]] +
                [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[0], anomaly_quantile, L, window_size(datasetId))]
                 for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
                 for L in [2, 4, 6]])
    elif datasetId == "IOT23-2":
        return ([[AnoFormerParams(K, 100, dim_feedforward, substitute_value, anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for K in [100, 200]
                 for dim_feedforward in [400, 900]
                 for substitute_value in getAFSubstituteValueFuncs(K)
                 for L in [4, 9]] +
                [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[0], anomaly_quantile, L, window_size(datasetId))]
                 for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
                 for L in [2, 4, 6]])
    elif datasetId == "SWAT":
        return ([[AnoFormerParams(K, 100, dim_feedforward, substitute_value, anomaly_quantile, 4, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for K in [100, 200]
                 for dim_feedforward in [400, 900]
                 for substitute_value in getAFSubstituteValueFuncs(K)] +
                [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[3], 0.99, 2, window_size(datasetId))]] +
                [[AnoFormerParams(200, 50, 900, getAFSubstituteValueFuncs(200)[3], 0.99, 6, window_size(datasetId))]])
    elif datasetId == "WADI":
        return ([[AnoFormerParams(50, 100, 200, substitute_value, anomaly_quantile, 2, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for substitute_value in getAFSubstituteValueFuncs(50)] +
                [[AnoFormerParams(100, 40, 300, getAFSubstituteValueFuncs(100)[0], anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for L in [2, 3]])
    else:
        return ([[AnoFormerParams(K, 100, dim_feedforward, substitute_value, anomaly_quantile, 1, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for K in [10, 20]
                 for dim_feedforward in [25, 50]
                 for substitute_value in getAFSubstituteValueFuncs(K)] +
                [[AnoFormerParams(100, d, 50, substitute_value, anomaly_quantile, L, window_size(datasetId))
                  for anomaly_quantile in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
                 for d in [20, 40]
                 for substitute_value in getAFSubstituteValueFuncs(100)
                 for L in [2, 4]])


def getAnoFormerBMParams(datasetId: str) -> list[list[AnoFormerParams]]:
    if datasetId == "EF42":
        return [[AnoFormerParams(200, 100, 400, getAFSubstituteValueFuncs(200)[3], 0.6, 4, window_size(datasetId))]]
    elif datasetId == "IOT23":
        return [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[0], 0.6, 4, window_size(datasetId))]]
    elif datasetId == "IOT23":
        return [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[0], 0.8, 4, window_size(datasetId))]]
    elif datasetId == "SWAT":
        return [[AnoFormerParams(200, 100, 900, getAFSubstituteValueFuncs(200)[1], 0.99, 4, window_size(datasetId))]]
    elif datasetId == "WADI":
        return [[AnoFormerParams(50, 100, 200, getAFSubstituteValueFuncs(50)[3], 0.5, 2, window_size(datasetId))]]
    else:
        return [[AnoFormerParams(10, 100, 50, getAFSubstituteValueFuncs(10)[0], 0.95, 1, window_size(datasetId))]]


def getMLstmPSParams(datasetId: str) -> list[list[MLSTMParams]]:
    if datasetId == "EF42":
        return [[MLSTMParams(40, 3, 0.001, clusterselection, window_size(datasetId), True, p, t_delta)
                 for clusterselection in [0, 2]
                 for p in [0.1, 1, 10, 100, 1000]
                 for t_delta in [50, 100, 150, 200]]]
    if datasetId == "IOT23" or datasetId == "IOT23-2":
        return [[MLSTMParams(40, 2, 0.01, clusterselection, window_size(datasetId), True, p, t_delta)
                 for clusterselection in [0, 2]
                 for p in [0.1, 1, 10, 100, 1000]
                 for t_delta in [50, 100, 150, 200]]]
    elif datasetId == "SWAT":
        return [[MLSTMParams(40, 3, 0.1, clusterselection, window_size(datasetId), True, p, t_delta)
                 for clusterselection in [0, 2]
                 for p in [120, 150, 175, 200, 250, 300, 500, 1000, 5000]
                 for t_delta in [50, 100, 150, 200]]]
    elif datasetId == "WAFER":
        return [[MLSTMParams(40, 3, 0.1, clusterselection, window_size(datasetId), True, p, t_delta)
                 for clusterselection in [0, 2]
                 for p in [3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15]
                 for t_delta in [50, 100, 150, 200]]]
    elif datasetId == "WADI":
        return [[MLSTMParams(hidden_size, 2, 0.05, clusterselection, window_size(datasetId), True, p, t_delta)
                 for clusterselection in [0, 2]
                 for p in [0.01, 0.1, 1, 10]
                 for t_delta in [50, 100, 150, 200]]
                for hidden_size in [40, 50]]


def getMlstmBMParams(datasetId: str) -> list[list[MLSTMParams]]:
    if datasetId == "EF42":
        return [[MLSTMParams(hidden_size=40, number_layers=3, thresh_stepsize=0.001, clusterselection=0, window_len=96,
                             pruning=True, p=1, t_delta=50)]]
    elif datasetId == "IOT23":
        return [[MLSTMParams(hidden_size=40, number_layers=2, thresh_stepsize=0.001, clusterselection=2, window_len=100,
                             pruning=pruning, p=0.1, t_delta=200)
                 for pruning in [False, True]]]
    elif datasetId == "IOT23-2":
        return [[MLSTMParams(hidden_size=40, number_layers=2, thresh_stepsize=0.001, clusterselection=2, window_len=100,
                             pruning=pruning, p=0.1, t_delta=200)
                 for pruning in [False, True]]]
    elif datasetId == "SWAT":
        return [[MLSTMParams(hidden_size=40, number_layers=3, thresh_stepsize=0.1, clusterselection=0, window_len=100,
                             pruning=True, p=20, t_delta=100)]]
    elif datasetId == "WADI":
        return [[MLSTMParams(hidden_size=40, number_layers=2, thresh_stepsize=0.05, clusterselection=2, window_len=100,
                             pruning=True, p=10, t_delta=50)]]
    elif datasetId == "WAFER":
        return [[MLSTMParams(hidden_size=40, number_layers=3, thresh_stepsize=0.1, clusterselection=2, window_len=100,
                             pruning=True, p=12, t_delta=150)]]


def getMtadGatBMParams(datasetId: str) -> list[list[MTAD_GATParams]]:
    if datasetId == "EF42":
        return [[MTAD_GATParams(gamma=1, recon_latent_dim=75, window_length=96)]]
    elif datasetId == "IOT23":
        return [[MTAD_GATParams(gamma=0.8, recon_latent_dim=25, window_length=100)]]
    elif datasetId == "IOT23-2":
        return [[MTAD_GATParams(gamma=1, recon_latent_dim=25, window_length=100)]]
    elif datasetId == "SWAT":
        return [[MTAD_GATParams(gamma=0.8, recon_latent_dim=25, window_length=100)]]
    elif datasetId == "WADI":
        return [[MTAD_GATParams(gamma=0.8, recon_latent_dim=75, window_length=100)]]
    elif datasetId == "WAFER":
        return [[MTAD_GATParams(gamma=0.4, recon_latent_dim=50, window_length=100)]]


def getTranVaeBMParams(datasetId: str) -> list[list[TranVAEParams]]:
    if datasetId == "EF42":
        return [[TranVAEParams(num_layers=2, kld_weight=0.005, window_length=96)]]
    elif datasetId == "IOT23":
        return [[TranVAEParams(num_layers=1, kld_weight=0.001, window_length=100)]]
    elif datasetId == "IOT23-2":
        return [[TranVAEParams(num_layers=2, kld_weight=1, window_length=100)]]
    elif datasetId == "SWAT":
        return [[TranVAEParams(num_layers=1, kld_weight=0.001, window_length=100)]]
    elif datasetId == "WADI":
        return [[TranVAEParams(num_layers=1, kld_weight=0.001, window_length=100)]]
    elif datasetId == "WAFER":
        return [[TranVAEParams(num_layers=1, kld_weight=0.02, window_length=100)]]


models: dict[str, ModelWrapper] = {
    "IF": ModelWrapper(
        IsolationForest,
        lambda model, epochs, lr: model.fit(),
        IsolationForest.getAnomalies,
        SINGLE_EPOCH_RANGE,
        SINGLE_EPOCH_RANGE,
        lambda _: [[EmptyParams()]],
        lambda _: [[EmptyParams()]]
    ),
    "AnoFormer": ModelWrapper(
        AnoFormer,
        AnoFormer.fit,
        lambda model: model.getAnomalies()[0],
        lambda datasetId: EpochRange(1, 1) if datasetId == "WADI" else EpochRange(5, 2),
        lambda datasetId: EpochRange(1, 5) if datasetId == "WADI" else EpochRange(1, 20),
        getAnoFormerPSParams,
        getAnoFormerBMParams,
        applyAnoFormerAnomalyParams,
        lambda model: model.test_pred_errs.tolist()
    ),
    "MLSTM": ModelWrapper(
        ModifiedLSTM,
        ModifiedLSTM.fit,
        lambda model: model.getAnomalies()[0],
        PS_DEFAULT_EPOCH_RANGE,
        EpochRange(50, 10),
        getMLstmPSParams,
        getMlstmBMParams,
        applyMLSTMAnomalyParams,
        lambda model: model._pred_errs.sum(dim=1).tolist()
    ),
    "MTAD_GAT": ModelWrapper(
        MTAD_GAT,
        MTAD_GAT.fit,
        lambda model: model.getAnomalies()[0][0],
        PS_DEFAULT_EPOCH_RANGE,
        EpochRange(50, 5),
        lambda datasetId: [
            [MTAD_GATParams(gamma, recon_latent_dim, window_size(datasetId))]
            for gamma in [0.4, 0.6, 0.8, 1.0]
            for recon_latent_dim in [25, 50, 75]
        ],
        getMtadGatBMParams,
        None,
        lambda model: [model.test_pred_df[feature].tolist() for feature in
                       ["A_Score_Global", "A_Forecast_Global", "A_Recon_Global"]]
    ),
    "TranVAE": ModelWrapper(
        TranVAE,
        TranVAE.fit,
        lambda model: model.getAnomalies()[0][0],
        EpochRange(100, 6),
        EpochRange(10, 200),
        lambda datasetId: [
            [TranVAEParams(num_layers, kld_weight, window_size(datasetId))]
            for num_layers in [1, 2]
            for kld_weight in [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.7, 0.1, 0.2, 0.5, 0.7, 1]
        ],
        getTranVaeBMParams,
        None,
        lambda model: np.concatenate((model._scores_test, np.zeros(max(model.Y_test_df.shape[0] - len(model._scores_test), 0)))).tolist()
    ),
    "AllFalse": ModelWrapper(
        AllFalse,
        AllFalse.fit,
        AllFalse.getAnomalies,
        SINGLE_EPOCH_RANGE,
        SINGLE_EPOCH_RANGE,
        lambda _: [[EmptyParams()]],
        lambda _: [[EmptyParams()]]
    ),
    "AllTrue": ModelWrapper(
        AllTrue,
        AllTrue.fit,
        AllTrue.getAnomalies,
        SINGLE_EPOCH_RANGE,
        SINGLE_EPOCH_RANGE,
        lambda _: [[EmptyParams()]],
        lambda _: [[EmptyParams()]]
    ),
    "Random": ModelWrapper(
        Random,
        Random.fit,
        Random.getAnomalies,
        SINGLE_EPOCH_RANGE,
        SINGLE_EPOCH_RANGE,
        lambda _: [[RandomParams(p) for p in [0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]],
        lambda _: [[RandomParams(p) for p in [0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]],
        applyRandomAnomalyParams
    ),
    "NPRandom": ModelWrapper(
        NPRandom,
        NPRandom.fit,
        NPRandom.getAnomalies,
        SINGLE_EPOCH_RANGE,
        SINGLE_EPOCH_RANGE,
        lambda _: [[EmptyParams()]],
        lambda _: [[EmptyParams()]]
    )
}

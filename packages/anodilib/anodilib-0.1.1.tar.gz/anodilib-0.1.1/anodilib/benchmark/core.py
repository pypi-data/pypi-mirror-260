import gc
import os
import sys
from datetime import datetime, timedelta

import pandas as pd
from fastai.torch_core import set_seed
from sklearn.metrics import f1_score, matthews_corrcoef

from param import BEST_PARAMS_FILE, BM_SCORES_FILE, PS_RAW_FILE, BM_RAW_FILE, PS_SCORES_FILE, datasets, models

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.algorithm import save
from metrics.cmetrics import c_f1_score, c_matthews_corrcoef, c_precision, c_recall
from metrics.pa.pointAdjustment import adjust_points, adjust_points_smoothing


def execBenchmark(paramSearch: bool = False, whitelist: list[tuple[str, str]] = None, blacklist: list[tuple[str, str]] = None):
    """
    executes a benchmarking run
    :param paramSearch: True to run the parameter search, False to run the actual benchmark
    :param whitelist: if not None, only the model-dataset-combinations from this list will be benchmarked
    :param blacklist: if not None, the model-dataset-combinations from this list will not be benchmarked
    """
    try:
        result = pd.read_pickle(PS_RAW_FILE if paramSearch else BM_RAW_FILE)
    except FileNotFoundError:
        result: pd.DataFrame = pd.DataFrame(
            columns=["model", "params", "dataset", "epoch", "prediction", "labels", "predErrs", "startTime", "endTime", "duration", "totalDuration",
                     "trainLoss", "predictDuration", "getAnomaliesDuration"])

    for modelId, modelWrapper in models.items():
        for datasetId, train_test in datasets.items():
            if (whitelist and (modelId, datasetId) not in whitelist) or (blacklist and (modelId, datasetId) in blacklist):
                continue
            parameterGroups = modelWrapper.getPSParams(datasetId) if paramSearch else modelWrapper.getBMParams(datasetId)
            epochRange = modelWrapper.psEpochRange(datasetId) if paramSearch else modelWrapper.bmEpochRange(datasetId)
            for parameterGroup in parameterGroups:
                if ((result["model"] == modelId) & (result["dataset"] == datasetId) & (result["params"] == parameterGroup[0].toString())).any():
                    continue
                print("init", modelId, parameterGroup[0].toString(), "on", datasetId)
                set_seed(31)
                model = modelWrapper.modelClass(**(parameterGroup[0].asdict()), dataset_specification=train_test[0],
                                                test_fraction=0.2 if len(train_test) == 1 else 0)
                totalDuration: timedelta = timedelta()

                for epoch in epochRange.getRange():
                    print("epoch:", epoch)
                    startTime: datetime = datetime.now()
                    modelWrapper.fit(model, epochRange.interval)
                    endTime: datetime = datetime.now()
                    try:
                        filename = f"{'ps' if paramSearch else 'bm'}_{modelId}_{datasetId}_{parameterGroup[0].toFilenameString()}_{epoch}"
                        save(model, filename, "objects/" + filename, False, False)
                    except:
                        pass
                    train_loss = getTrainLoss(model, epochRange.interval)

                    duration: timedelta = endTime - startTime
                    totalDuration = totalDuration + duration

                    predictStartTime = datetime.now()
                    model.predict(train_test[1] if len(train_test) == 2 else None)
                    predictDuration = datetime.now() - predictStartTime
                    predErrs = modelWrapper.getPredErrors(model)

                    for anomalyParameters in parameterGroup:
                        if modelWrapper.applyPSAnomalyParam:
                            modelWrapper.applyPSAnomalyParam(model, anomalyParameters)
                        getAnomaliesStartTime = datetime.now()
                        prediction = modelWrapper.getAnomalies(model).astype(bool).tolist()
                        getAnomaliesDuration = datetime.now() - getAnomaliesStartTime
                        labels = model.Y_test_df.iloc[:, 0].astype(bool).tolist()
                        assert len(prediction) == len(labels), "prediction and labels differ in shape"
                        result = pd.concat([result, pd.DataFrame(
                            data=[
                                [modelId, anomalyParameters.toString(), datasetId, epoch, prediction, labels, predErrs, startTime, endTime, duration,
                                 totalDuration, train_loss, predictDuration, getAnomaliesDuration]],
                            columns=result.columns)])
                try:
                    result.reset_index(drop=True, inplace=True)
                    result.to_pickle(f"anodi/benchmark/files/intermediate/{'ps' if paramSearch else 'bm'}_raw_{modelId}_{datasetId}.pkl")
                except Exception:
                    print("could not save intermediate result")
                del model
                gc.collect()

    result.to_pickle(PS_RAW_FILE if paramSearch else BM_RAW_FILE)


def getTrainLoss(model, epochInterval: int):
    """
    tries to extract the current train-loss from the given model
    :param model: the model
    :param epochInterval: The epoch interval of the current benchmark run. This function will try to extract exactly epochInterval losses
    :return: a list of length epochInterval containing the last train-loss for each epoch
    """
    try:
        interval = len(model.learner.recorder.losses) // epochInterval
        return list(map(lambda tensor: tensor.tolist(), model.learner.recorder.losses[interval - 1::interval]))
    except Exception:
        return None


def addScores(paramSearch: bool = False, saveCsv: bool = False, csvColumns: list[str] = None):
    """
    computes scores for the predictions in the raw file
    :param paramSearch: True to compute the parameter search scores, False for actual benchmark scores
    :param saveCsv: True if the results should also be saved as a csv file
    :param csvColumns: if not None, the csv file will only contain the given subset of columns
    """
    result: pd.DataFrame = pd.read_pickle(PS_RAW_FILE if paramSearch else BM_RAW_FILE)

    def getScores(row: pd.Series):
        paPred = adjust_points(row.prediction, row.labels)
        spaPred = adjust_points_smoothing(row.prediction, row.labels)
        f1 = f1_score(row.labels, row.prediction)
        paf1 = f1_score(row.labels, paPred)
        spaf1 = c_f1_score(spaPred, row.labels)
        mcc = matthews_corrcoef(row.labels, row.prediction)
        pamcc = matthews_corrcoef(row.labels, paPred)
        spamcc = c_matthews_corrcoef(spaPred, row.labels)
        precision = c_precision(row.prediction, row.labels)
        paPrecision = c_precision(paPred, row.labels)
        spaPrecision = c_precision(spaPred, row.labels)
        recall = c_recall(row.prediction, row.labels)
        paRecall = c_recall(paPred, row.labels)
        spaRecall = c_recall(spaPred, row.labels)
        return pd.Series(
            [f1, paf1, spaf1, mcc, pamcc, spamcc, precision, paPrecision, spaPrecision, recall, paRecall, spaRecall],
            index=["f1", "paf1", "spaf1", "mcc", "pamcc", "spamcc", "precision", "paPrecision", "spaPrecision", "recall", "paRecall", "spaRecall"])

    result = pd.concat([result, result.apply(getScores, axis=1)], axis=1)
    result.to_pickle(PS_SCORES_FILE if paramSearch else BM_SCORES_FILE)
    if saveCsv:
        if csvColumns is not None:
            result = result[csvColumns]
        result.sort_values(["model", "dataset", "params", "epoch"]).to_csv(f"anodi/benchmark/files/{'ps' if paramSearch else 'bm'}_scores.csv")


def getBestParams():
    """
    calculates the parameters and epoch at which the highest score was achieved for each model, each dataset and each score
    """
    psResult: pd.DataFrame = pd.read_pickle(PS_SCORES_FILE)
    resultByScore = [
        psResult[["model", "dataset", "params", "epoch", score]]
        .sort_values(score, ascending=False)
        .drop_duplicates(["model", "dataset"])
        for score in ["f1", "paf1", "spaf1", "mcc", "pamcc", "spamcc"]
    ]
    result = pd.concat(resultByScore, ignore_index=True).sort_values(["model", "dataset"]).reset_index(drop=True)
    result.to_csv(BEST_PARAMS_FILE)

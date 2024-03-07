import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from param import models, datasets


def plotScorePerAlgAndDataset(scoresFilename: str, scores: list[str], pngFilename: str = None, maxByScore: str = None, removeModels: list[str] = None,
                              max_rows: int = 3):
    """
    Plots the maximum scores for each model and each dataset individually. The resulting plot is a grid of subplots, one for each score.
    :param scoresFilename: name of the scores-file to be used
    :param scores: list of scores to plot
    :param pngFilename: filename of the resulting image
    :param maxByScore: if not None, all entries
    :param removeModels: models to be excluded in the plot
    :param max_rows: maximum number of rows for the grid of subplots
    """
    pngFilename = pngFilename or scoresFilename + ("_by_" + maxByScore) if maxByScore else "_max"
    df: pd.DataFrame = pd.read_pickle("anodi/benchmark/files/" + scoresFilename + ".pkl")
    if maxByScore is not None:
        df = df.sort_values(maxByScore, ascending=False).drop_duplicates(["model", "dataset"])
    X_axis = np.arange(len(datasets))
    modelIds = list(models.keys())
    if removeModels is not None:
        for removeModel in removeModels:
            modelIds.remove(removeModel)
    bar_width = 1 / (len(modelIds) + 3)
    cols = math.ceil(len(scores) / max_rows)
    rows = min(len(scores), max_rows)
    fig, subplots = plt.subplots(rows, cols, figsize=(10 * cols, 3 * rows), sharex=True)
    plt.xticks(X_axis, datasets.keys())
    for score, subplot in zip(scores, (subplots.T.flatten() if hasattr(subplots, "T") else [subplots])):
        for idx, modelId in enumerate(modelIds):
            scores = [df[(df["model"] == modelId) & (df["dataset"] == datasetId)][score].max() for datasetId in datasets.keys()]
            offset = (idx - (len(modelIds) - 1) / 2) / (len(modelIds) + 3)
            subplot.bar(X_axis + offset, scores, bar_width, label=modelId)

        subplot.set_ylabel(score)
        if score[-2:] == "f1":
            subplot.set_ylim([0, 1])
        elif score[-3:] == "mcc":
            subplot.set_ylim([-1, 1])
    plt.legend(loc="lower right", bbox_to_anchor=(1.2, 0))
    plt.savefig("anodi/benchmark/plot/" + pngFilename + ".png", bbox_inches="tight")


def plotLabels(scoresFilename: str, model: str, dataset: str, epoch: int = None, params: str = None, maxByScore: str = None, pngFilename: str = None,
               plotPredErrs: bool = True, yScale: str = "linear", interval: tuple[int, int] = None, title="Comparison between predicted labels vs true labels"):
    """
    visualizes the labels and prediction
    :param scoresFilename: name of the scores-file
    :param model: model name
    :param dataset: dataset name
    :param epoch: epoch number (optional)
    :param params: the parameter string representation (optional)
    :param maxByScore: if not None, use the best matching row based on the given score
    :param pngFilename: filename of the resulting image
    :param plotPredErrs: True to also plot the prediction errors
    :param yScale: linear, log
    :param interval: if passed, the interval of timestamps to be included
    :param title: title
    """
    pngFilename = pngFilename or scoresFilename + "_" + model + "_" + dataset + ("_by_" + maxByScore) if maxByScore else ""
    df = pd.read_pickle("anodi/benchmark/files/" + scoresFilename + ".pkl")
    df = df[(df.model == model) & (df.dataset == dataset)]
    if epoch is not None:
        df = df[df.epoch == epoch]
    if params is not None:
        df = df[df.params == params]
    if maxByScore is not None:
        df = df.sort_values(maxByScore, ascending=False)
        df = df.iloc[[0]] if len(df) != 0 else df
    assert len(df) == 1, ("Could not find exactly one row matching the filter. Found: " + str(len(df)))
    df = df.iloc[0]
    true_labels = df.labels if not interval else df.labels[interval[0]:interval[1]]
    predicted_labels = df.prediction if not interval else df.prediction[interval[0]:interval[1]]
    _, ax = plt.subplots(figsize=(20, 8))
    true_labels = list(map(lambda x: 1 if x else 0, true_labels))
    predicted_labels = list(map(lambda x: 1 if x else 0, predicted_labels))
    x = range(1, len(true_labels) + 1)
    ax.step(x, true_labels, label="true label", alpha=0.75)
    ax.step(x, predicted_labels, label="predicted label", alpha=0.75)
    if plotPredErrs and df.predErrs is not None:
        predErrs = np.asarray(df.predErrs if not interval else df.predErrs[interval[0]:interval[1]])
        predErrs = np.concatenate((predErrs, np.zeros(len(true_labels) - len(predErrs))))
        predErrs /= predErrs.max()
        ax.step(x, predErrs, label="pred errs", alpha=0.75)
    # add color highlighting
    for i in range(len(true_labels)):
        if predicted_labels[i] == true_labels[i]:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='green', alpha=0.3)
        else:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='red', alpha=0.3)
    ax.set_xlabel('timestep')
    ax.set_ylabel('label')
    ax.set_title(title + "\n" + model + " on " + dataset)
    plt.yticks([0, 1])
    ax.set_yscale(yScale)
    ax.legend()
    plt.savefig("anodi/benchmark/plot/" + pngFilename + ".png")


plotScorePerAlgAndDataset("ps_scores",
                          ["f1", "paf1", "spaf1", "mcc", "pamcc", "spamcc", "precision", "paPrecision", "spaPrecision", "recall", "paRecall", "spaRecall"],
                          "ps_scores", "spaf1", ["AllFalse"])
plotScorePerAlgAndDataset("bm_scores",
                          ["f1", "paf1", "spaf1", "mcc", "pamcc", "spamcc", "precision", "paPrecision", "spaPrecision", "recall", "paRecall", "spaRecall"],
                          "bm_scores", "spaf1", ["AllFalse"])

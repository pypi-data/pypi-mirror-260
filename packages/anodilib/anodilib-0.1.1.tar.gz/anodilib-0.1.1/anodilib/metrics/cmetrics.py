from math import sqrt
import numpy as np


def c_fbeta_score(
    pred: list[bool | float],
    labels: list[bool | float],
    beta: float = 1,
    zero_division=0,
):
    """
    computes the confidence f-beta-score, a non-boolean extension of the f-beta-score

    parameters:
        pred: predicted probabilities of an anomaly in range [0, 1]
        labels: ground truth labels
        beta: weight of recall, defaults to 1
        zero_division: value to return in case of a zero division
    returns:
        confidence f-beta-score
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = np.asarray(pred)
    labels = np.asarray(labels)
    tp = (pred * labels).sum()
    fn = ((1 - pred) * labels).sum()
    fp = (pred * (1 - labels)).sum()

    if tp == 0:
        return zero_division

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return (1 + beta * beta) * precision * recall / (beta * beta * precision + recall)


def c_f1_score(pred: list[float], labels: list[bool], zero_division=0):
    """
    computes the confidence f1-score, a non-boolean extension of the f1-score

    parameters:
        pred: predicted probabilities of an anomaly in range [0, 1]
        labels: ground truth labels
        zero_division: value to return in case of a zero division
    returns:
        confidence f1-score
    """
    return c_fbeta_score(pred, labels, 1, zero_division)


def c_precision(pred: list[float], labels: list[bool], zero_division=0):
    """
    computes the confidence precision, a non-boolean extension of the precision score

    parameters:
        pred: predicted probabilities of an anomaly in range [0, 1]
        labels: ground truth labels
        zero_division: value to return in case of a zero division
    returns:
        confidence precision
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = np.asarray(pred)
    labels = np.asarray(labels)
    tp = (pred * labels).sum()
    fp = (pred * (1 - labels)).sum()

    return zero_division if tp + fp == 0 else tp / (tp + fp)


def c_recall(pred: list[float], labels: list[bool], zero_division=0):
    """
    computes the confidence recall, a non-boolean extension of the recall score

    parameters:
        pred: predicted probabilities of an anomaly in range [0, 1]
        labels: ground truth labels
        zero_division: value to return in case of a zero division
    returns:
        confidence recall
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = np.asarray(pred)
    labels = np.asarray(labels)
    tp = (pred * labels).sum()
    fn = ((1 - pred) * labels).sum()

    return zero_division if tp + fn == 0 else tp / (tp + fn)


def c_matthews_corrcoef(pred: list[float], labels: list[bool]):
    """
    computes the Matthews correlation coefficient (MCC)

    parameters:
        pred: predicted probabilities of an anomaly in range [0, 1]
        labels: ground truth labels
    returns:
        confidence MCC
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = np.asarray(pred)
    labels = np.asarray(labels)
    tp = (pred * labels).sum()
    fn = ((1 - pred) * labels).sum()
    fp = (pred * (1 - labels)).sum()
    tn = ((1 - pred) * (1 - labels)).sum()

    return (tp * tn - fp * fn) / sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

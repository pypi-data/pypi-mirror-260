from typing import Callable
import math


def adjust_points(pred: list[bool], labels: list[bool]):
    """
    Applies default point adjustment.\\
    An anomaly segment is adjusted along its entire length if at least one point within the segment is detected correctly.

    parameters:
        pred: predicted anomalies
        labels: ground truth labels
    returns:
        adjusted prediction
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = pred.copy()
    i = 0
    while i < len(pred):
        if pred[i] and labels[i]:
            for j in range(i, 0, -1):
                if not labels[j]:
                    break
                else:
                    pred[j] = True

            while i < len(pred) and labels[i]:
                pred[i] = True
                i += 1
        else:
            i += 1
    return pred


def adjust_points_percent_k(pred: list[bool], labels: list[bool], k: float):
    """
    Applies k-percent point adjustment.\\
    An anomaly segment is adjusted along its entire length if
        TP / segment_length > k,
    where TP is the number of correctly detected points within the segment.

    parameters:
        pred: predicted anomalies
        labels: ground truth labels
        k: float in range [0, 1]
    returns:
        adjusted prediction
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = pred.copy()
    i = 0
    while i < len(pred):
        if labels[i]:
            j = i + 1
            predictCount = 1
            while j < len(pred) and labels[j]:
                if pred[j]:
                    predictCount += 1
                j += 1

            if predictCount / (j - i) > k:
                for m in range(i, j):
                    pred[m] = True

            i = j
        else:
            i += 1
    return pred


def adjust_points_decay_func(
    pred: list[float | bool], labels: list[bool], decay_func: Callable[[int], float]
):
    """
    Applies point adjustment with decay function.

    parameters:
        pred: predicted probabilities of an anomaly or boolean predictions
        labels: ground truth labels
        decay_func: decay function, monotone decreasing, decay_func(0) has to be equal to 1, has to be defined for all integers in range [0, len(pred) - 1]
    returns:
        adjusted prediction
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = pred.copy()
    i = 0
    while i < len(pred):
        if labels[i]:
            j = i
            prod_p = 1
            recall = 0
            while j < len(pred) and labels[j]:
                recall += decay_func(j - i) * pred[j] * prod_p
                prod_p *= 1 - pred[j]
                j += 1

            while i < j:
                pred[i] = recall
                i += 1
        else:
            pred[i] = float(pred[i])
            i += 1
    return pred


def adjust_points_smoothing(pred: list[bool], labels: list[bool]):
    """
    Applies smoothing point adjustment with linear rewarding.

    parameters:
        pred: predicted anomalies
        labels: ground truth labels
    returns:
        adjusted prediction
    """
    if len(pred) != len(labels):
        raise ValueError
    pred = pred.copy()
    i = 0
    while i < len(pred):
        if labels[i]:
            t_1 = -1
            detectedCount = 0
            j = i
            while j < len(pred) and labels[j]:
                if pred[j]:
                    detectedCount += 1
                    if t_1 == -1:
                        t_1 = j
                j += 1

            P_m = math.ceil(detectedCount * (j - t_1) / (j - i))
            R_t1 = 1 - (t_1 - i) / (j - i)
            for k in range(i, j):
                if t_1 == -1 or k < t_1:
                    pred[k] = 0
                elif pred[k]:
                    pred[k] = R_t1
                elif k < t_1 + P_m:
                    pred[k] = 1 - (k - i) / (j - i)
                else:
                    pred[k] = 0

            i = j
        else:
            pred[i] = float(pred[i])
            i += 1
    return pred

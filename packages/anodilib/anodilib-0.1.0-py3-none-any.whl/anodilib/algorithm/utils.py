import math

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from algorithm.spot import SPOT


def slide_window_view(df, window_length: int, stride: int = 1):
    _windows = np.lib.stride_tricks.sliding_window_view(df, window_length, axis=0)
    _windows = _windows[::stride, :, :]

    return _windows


def mahalanobis_distance(X, cov=None, mu=None):
    if mu is None:
        mu = np.mean(X, axis=0)
    if cov is None:
        cov = np.cov(X, rowvar=False)
    try:
        inv_cov = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        print("Error, probably singular matrix!")
        inv_cov = np.eye(cov.shape[0])

    X_diff_mu = X - mu
    M = np.apply_along_axis(
        lambda x: np.matmul(np.matmul(x, inv_cov), x.T), 1, X_diff_mu
    )
    return M


"""
LSTMcalcErrorThreshold is used to determine the thresholding value where errors between predicted value and actual 
value will be considered anomalous. 
cluster_selection takes values [0,1,2]
0 is the standard method, chooses out of three the cluster with highest errors
1 can be used if extreme values makes the default set too small
2 is an option to use both prior sets together for experimenting
"""


def LSTMcalcErrorThreshold(error_seq, input_length=5, d=0.5, cluster_selection=0, pruning=False, verbose=True, p=0.05, t_delta=50):
    # prune first t >= input_length values in error_seq

    error_set = error_seq[input_length:]

    # sometimes throws error about putting in misshaped sequence into array, try fitting data types
    c1 = 0
    c2 = float(error_set.mean().iloc[0])
    c3 = float(error_set.max().iloc[0])
    startpts = np.array([c1, c2, c3]).reshape(-1, 1)

    kmeans = KMeans(n_clusters=3, init=startpts, n_init=1).fit(error_set)

    # assumption: cluster with index 2 is always that with largest error values -> for EF42 dataset it has only one value with massive error!
    if (cluster_selection == 0):
        error_cluster = error_set[kmeans.labels_ == 2]
    elif (cluster_selection == 1):
        error_cluster = error_set[kmeans.labels_ == 1]
    elif (cluster_selection == 2):
        error_cluster = error_set[kmeans.labels_ >= 1]
    else:
        print("Parameter cluster_selection is not a valid option, process failed")
        return 0.0

    # now we obtain the initial error threshold
    f_s = float(error_cluster.min().iloc[0])

    # for calculating k_max we obtain the largest value inside the error_cluster
    max_error = float(error_cluster.max().iloc[0])

    error_val_range = max_error - f_s

    k_max = math.ceil(error_val_range / d)

    # calculate candidate thresholds f_k
    k_range = range(k_max + 1)

    f_k_list = [f_s + k * d for k in k_range]
    error_set = error_set["Numbers"].to_numpy()
    std_error_set = np.std(error_set)

    max_T = None
    max_f_k = None
    last_ea_indices = None
    prune_indices = LSTM_prune_indices(error_set, p, t_delta) if pruning else None
    for f_k in f_k_list:
        ea_indices: np.ndarray = error_set > f_k
        if np.array_equal(ea_indices, last_ea_indices):
            continue
        last_ea_indices = ea_indices

        E_N = error_set[~ea_indices]
        if pruning:
            ea_indices = ea_indices & ~prune_indices

        n_A = max(ea_indices.sum(), 5)

        T = float((std_error_set / np.std(E_N)) * (1 / n_A))
        if max_T is None or T > max_T:
            max_T = T
            max_f_k = f_k

    return max_f_k, f_s


# p is limit for absolute difference in errors, delta is limit for difference in time
# p and delta will need to be determined by experiment
# p and delta need to be set, can vary between datasets!
def LSTM_prune_indices(error_seq: np.ndarray, p: float, delta: int) -> np.ndarray:
    if len(error_seq) == 0:
        return error_seq
    error_seq = error_seq.astype(float)
    # pad the sequence with _delta_ nan on both sides
    padded_seq = np.pad(error_seq, (delta, delta), 'constant', constant_values=np.nan)
    # rolling window, for each element the window contains _delta_ elements in both directions and the element itself
    windows = np.lib.stride_tricks.sliding_window_view(padded_seq, 2 * delta + 1)
    # absolute difference of each element in the window to the center element
    diff = np.abs(windows - error_seq[np.newaxis].T)
    # return True when the difference for at least one element in the window is smaller than p
    # check for >1 occurrences since the element is part of the window (diff = 0)
    return np.sum(diff < p, axis=1) > 1


def adjust_anomaly_scores(scores, dataset, is_train, lookback):
    """
    Method for MSL and SMAP where channels have been concatenated as part of the preprocessing
    :param scores: anomaly_scores
    :param dataset: name of dataset
    :param is_train: if scores is from train set
    :param lookback: lookback (window size) used in model
    """

    # Remove errors for time steps when transition to new channel (as this will be impossible for model to predict)
    if dataset.upper() not in ['SMAP', 'MSL']:
        return scores

    adjusted_scores = scores.copy()
    if is_train:
        md = pd.read_csv(f'./datasets/data/{dataset.lower()}_train_md.csv')
    else:
        md = pd.read_csv('./datasets/data/labeled_anomalies.csv')
        md = md[md['spacecraft'] == dataset.upper()]

    md = md[md['chan_id'] != 'P-2']

    # Sort values by channel
    md = md.sort_values(by=['chan_id'])

    # Getting the cumulative start index for each channel
    sep_cuma = np.cumsum(md['num_values'].values) - lookback
    sep_cuma = sep_cuma[:-1]
    buffer = np.arange(1, 20)
    i_remov = np.sort(np.concatenate((sep_cuma, np.array([i + buffer for i in sep_cuma]).flatten(),
                                      np.array([i - buffer for i in sep_cuma]).flatten())))
    i_remov = i_remov[(i_remov < len(adjusted_scores)) & (i_remov >= 0)]
    i_remov = np.sort(np.unique(i_remov))
    if len(i_remov) != 0:
        adjusted_scores[i_remov] = 0

    # Normalize each concatenated part individually
    sep_cuma = np.cumsum(md['num_values'].values) - lookback
    s = [0] + sep_cuma.tolist()
    for c_start, c_end in [(s[i], s[i + 1]) for i in range(len(s) - 1)]:
        e_s = adjusted_scores[c_start: c_end + 1]

        e_s = (e_s - np.min(e_s)) / (np.max(e_s) - np.min(e_s))
        adjusted_scores[c_start: c_end + 1] = e_s

    return adjusted_scores


def find_epsilon(errors, reg_level=1):
    """
    Threshold method proposed by Hundman et. al. (https://arxiv.org/abs/1802.04431)
    Code from TelemAnom (https://github.com/khundman/telemanom)
    """
    e_s = errors
    best_epsilon = None
    max_score = -10000000
    mean_e_s = np.mean(e_s)
    sd_e_s = np.std(e_s)

    for z in np.arange(2.5, 12, 0.5):
        epsilon = mean_e_s + sd_e_s * z
        pruned_e_s = e_s[e_s < epsilon]

        i_anom = np.argwhere(e_s >= epsilon).reshape(-1,)
        buffer = np.arange(1, 50)
        i_anom = np.sort(
            np.concatenate(
                (
                    i_anom,
                    np.array([i + buffer for i in i_anom]).flatten(),
                    np.array([i - buffer for i in i_anom]).flatten(),
                )
            )
        )
        i_anom = i_anom[(i_anom < len(e_s)) & (i_anom >= 0)]
        i_anom = np.sort(np.unique(i_anom))

        if len(i_anom) > 0:
            # groups = [list(group) for group in mit.consecutive_groups(i_anom)]
            # E_seq = [(g[0], g[-1]) for g in groups if not g[0] == g[-1]]

            mean_perc_decrease = (mean_e_s - np.mean(pruned_e_s)) / mean_e_s
            sd_perc_decrease = (sd_e_s - np.std(pruned_e_s)) / sd_e_s
            if reg_level == 0:
                denom = 1
            elif reg_level == 1:
                denom = len(i_anom)
            elif reg_level == 2:
                denom = len(i_anom) ** 2

            score = (mean_perc_decrease + sd_perc_decrease) / denom

            if score >= max_score and len(i_anom) < (len(e_s) * 0.5):
                max_score = score
                best_epsilon = epsilon

    if best_epsilon is None:
        best_epsilon = np.max(e_s)
    return best_epsilon


def epsilon_eval(train_scores, test_scores, test_labels, reg_level=1):
    best_epsilon = find_epsilon(train_scores, reg_level)
    pred, p_latency = adjust_predicts(test_scores, test_labels, best_epsilon, calc_latency=True)
    if test_labels is not None:
        p_t = calc_point2point(pred, test_labels)
        return {
            "f1": p_t[0],
            "precision": p_t[1],
            "recall": p_t[2],
            "TP": p_t[3],
            "TN": p_t[4],
            "FP": p_t[5],
            "FN": p_t[6],
            "threshold": best_epsilon,
            "latency": p_latency,
            "reg_level": reg_level,
        }, pred
    else:
        return {"threshold": best_epsilon, "reg_level": reg_level}


def pot_eval(init_score, score, label, q=1e-3, level=0.8, dynamic=False, min_extrema=True, verbose=True):
    """
    Run POT method on given score.
    :param init_score (np.ndarray): The data to get init threshold.
                    For `OmniAnomaly`, it should be the anomaly score of train set.
    :param: score (np.ndarray): The data to run POT method.
                    For `OmniAnomaly`, it should be the anomaly score of test set.
    :param label (np.ndarray): boolean list of true anomalies in score
    :param q (float): Detection level (risk)
    :param level (float): Probability associated with the initial threshold t
    :return dict: pot result dict
    Method from OmniAnomaly (https://github.com/NetManAIOps/OmniAnomaly)
    """

    if verbose:
        print(f"Running POT with q={q}, level={level}..")
    s = SPOT(q)  # SPOT object
    s.fit(init_score, score)
    s.initialize(level=level, min_extrema=min_extrema, verbose=verbose)  # Calibration step
    ret = s.run(dynamic=dynamic, with_alarm=False)

    if verbose:
        print(len(ret["alarms"]))
        print(len(ret["thresholds"]))

    pot_th = np.mean(ret["thresholds"])  # former -np.mean cause min_extrema change from True to False in old github-code in utils.pot_eval
    # check if threshold out of score-range
    if pot_th > score.max() or pot_th < score.min():
        pot_th = np.quantile(init_score, level)
    pred, p_latency = adjust_predicts(score, label, pot_th, calc_latency=True)
    if label is not None:
        p_t = calc_point2point(pred, label)
        return {
            "f1": p_t[0],
            "precision": p_t[1],
            "recall": p_t[2],
            "TP": p_t[3],
            "TN": p_t[4],
            "FP": p_t[5],
            "FN": p_t[6],
            "threshold": pot_th,
            "latency": p_latency,
        }
    else:
        return {
            "threshold": pot_th,
        }


def bf_search(score, label, start, end=None, step_num=1, display_freq=1, verbose=True):
    """
    Find the best-f1 score by searching best `threshold` in [`start`, `end`).
    Method from OmniAnomaly (https://github.com/NetManAIOps/OmniAnomaly)
    """

    if verbose:
        print("Finding best f1-score by searching for threshold..")
    if step_num is None or end is None:
        end = start
        step_num = 1
    search_step, search_range, search_lower_bound = step_num, end - start, start
    if verbose:
        print("search range: ", search_lower_bound, search_lower_bound + search_range)
    threshold = search_lower_bound
    m = (-1.0, -1.0, -1.0)
    m_t = 0.0
    m_l = 0
    for i in range(search_step):
        threshold += search_range / float(search_step)
        target, latency = calc_seq(score, label, threshold)
        if target[0] > m[0]:
            m_t = threshold
            m = target
            m_l = latency
        if verbose and i % display_freq == 0:
            print("cur thr: ", threshold, target, m, m_t)

    return {
        "f1": m[0],
        "precision": m[1],
        "recall": m[2],
        "TP": m[3],
        "TN": m[4],
        "FP": m[5],
        "FN": m[6],
        "threshold": m_t,
        "latency": m_l,
    }


def calc_seq(score, label, threshold):
    predict, latency = adjust_predicts(score, label, threshold, calc_latency=True)
    return calc_point2point(predict, label), latency


def calc_point2point(predict, actual):
    """
    calculate f1 score by predict and actual.
    Args:
            predict (np.ndarray): the predict label
            actual (np.ndarray): np.ndarray
    Method from OmniAnomaly (https://github.com/NetManAIOps/OmniAnomaly)
    """
    TP = np.sum(predict * actual)
    TN = np.sum((1 - predict) * (1 - actual))
    FP = np.sum(predict * (1 - actual))
    FN = np.sum((1 - predict) * actual)
    precision = TP / (TP + FP + 0.00001)
    recall = TP / (TP + FN + 0.00001)
    f1 = 2 * precision * recall / (precision + recall + 0.00001)
    return f1, precision, recall, TP, TN, FP, FN


def adjust_predicts(score, label, threshold, pred=None, calc_latency=False):
    """
    Calculate adjusted predict labels using given `score`, `threshold` (or given `pred`) and `label`.
    Args:
            score (np.ndarray): The anomaly score
            label (np.ndarray): The ground-truth label
            threshold (float): The threshold of anomaly score.
                    A point is labeled as "anomaly" if its score is lower than the threshold.
            pred (np.ndarray or None): if not None, adjust `pred` and ignore `score` and `threshold`,
            calc_latency (bool):
    Returns:
            np.ndarray: predict labels
    Method from OmniAnomaly (https://github.com/NetManAIOps/OmniAnomaly)
    """
    if label is None:
        predict = score > threshold
        return predict, None

    if pred is None:
        if len(score) != len(label):
            raise ValueError("score and label must have the same length")
        predict = score > threshold
    else:
        predict = pred

    actual = label > 0.1
    anomaly_state = False
    anomaly_count = 0
    latency = 0

    for i in range(len(predict)):
        if any(actual[max(i, 0): i + 1]) and predict[i] and not anomaly_state:
            anomaly_state = True
            anomaly_count += 1
            for j in range(i, 0, -1):
                if not actual[j]:
                    break
                else:
                    if not predict[j]:
                        predict[j] = True
                        latency += 1
        elif not actual[i]:
            anomaly_state = False
        if anomaly_state:
            predict[i] = True
    if calc_latency:
        return predict, latency / (anomaly_count + 1e-4)
    else:
        return predict

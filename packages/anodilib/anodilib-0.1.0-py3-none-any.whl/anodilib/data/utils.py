import numpy as np
import pyarrow.parquet as pq
import pandas
import os
from pathlib import Path
from sklearn.model_selection import train_test_split as sklearn_train_test_split


def slide_window_view(df, window_length: int, stride: int = 1):
    _windows = np.lib.stride_tricks.sliding_window_view(df, window_length, axis=0)
    _windows = _windows[::stride, :, :]

    return _windows


def load_to_pandas(path, columns: list = None):
    _table = pq.read_pandas(path, columns=columns)

    return _table.to_pandas()


def train_test_split(
    test_fraction: float,
    keep_time_relation: bool,
    X: pandas.DataFrame,
    y: pandas.DataFrame,
):
    if keep_time_relation:
        test_size = int(test_fraction * X.shape[0])
        train_size = X.shape[0] - test_size
        train_X = X.head(train_size)
        train_y = y.head(train_size)
        test_X = X.tail(test_size)
        test_y = y.tail(test_size)
        return train_X, train_y, test_X, test_y
    else:
        train_X, test_X, train_y, test_y = sklearn_train_test_split(
            X, y, test_size=test_fraction
        )
        return train_X, train_y, test_X, test_y


def get_project_data_directory():
    """
    Builds and returns the absolute path of the project directory.
    """
    # Get this files (test file) path, split it by '/' and reverse the resulting list.
    split_path = str(Path(__file__)).split(os.path.sep)
    split_path.reverse()
    index = split_path.index("anodi")

    return Path(__file__).parents[index]

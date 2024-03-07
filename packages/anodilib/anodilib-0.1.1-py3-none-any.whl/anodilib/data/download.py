import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import urllib.request
import numpy as np
from tsai.all import TSDataLoaders, TSDatasets
import pandas
from data.utils import slide_window_view
from data.DatasetSpecification import DatasetSpecification, EF42_TEST_SYN_V2_18

DATASETS_DIRECTORY = "data"


def is_url(string: str):
    if string is None:
        return False
    # pattern = r"^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$"
    # return bool(re.match(pattern, string)) this was somehow blocking the cpu
    return string.startswith("https")


def _get_data_from_url(url: str):
    print("Downloading dataset from url " + url)
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode("utf-8")


def _derive_path_from_specification(specification: DatasetSpecification):
    if specification.location is not None and not is_url(specification.location):
        return specification.location
    else:
        return (
            os.path.join(os.path.dirname(__file__), DATASETS_DIRECTORY)
            + os.sep
            + specification.dataset_name
        )


def _save_file_content(path: str, data: str):
    print("Saving dataset to path " + path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(data)


def _is_cached(specification: DatasetSpecification):
    return os.path.isfile(_derive_path_from_specification(specification))


def _maybe_cache_specification(specification: DatasetSpecification):
    path = _derive_path_from_specification(specification)
    if path is not None and not _is_cached(specification):
        if not is_url(specification.location):
            return  # in this case the dataset is adressed with a local path and should already be in the data directory
        data = _get_data_from_url(specification.location)
        _save_file_content(path, data)


def parse_dataset(path: str, specification: DatasetSpecification):
    df = None
    if not path.endswith("parquet"):
        df = pandas.read_csv(
            path,
            delimiter=specification.delimiter,
            skip_blank_lines=True,
            skipfooter=specification.skip_footer,
            header=None,
            skiprows=specification.skip_header,
            on_bad_lines='skip',
            decimal=specification.decimal,
        )
    else:
        df = pandas.read_parquet(path, "pyarrow", specification.columns)
    # replace date columns by timestamp if there are any
    for column in df.columns:
        if pandas.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = pandas.to_datetime(df[column]).astype("int64")
            print(str(column))
    X = None
    X = df.iloc[
        :, np.array(list(map(specification.is_data_column, range(len(df.columns)))))
    ]
    y = df.iloc[:, [specification.label_column]].copy()
    # only include numeric and boolean columns
    X = X.select_dtypes(include=[np.number, bool])
    # y = y.select_dtypes(include=[np.number, bool])
    # transform labels to 0 and 1
    y.replace(
        {
            specification.label_realizations[0]: 0,
            specification.label_realizations[1]: 1,
        },
        inplace=True,
    )
    if (
        specification.only_first_n_entries is not None
        and specification.only_first_n_entries != -1
    ):
        return (
            X.head(specification.only_first_n_entries),
            y.head(specification.only_first_n_entries),
            TSDatasets(
                X.head(specification.only_first_n_entries),
                y.head(specification.only_first_n_entries),
            ),
        )
    return (X, y, None)  # could return TSDatasets(X, y) in third component if necessary


# this is the method used by algorithm.py
def get_specification_as_pandas_dataframes(specification: DatasetSpecification):
    if specification.predefined_dataset is not None:
        X, y = specification.predefined_dataset
        return X, y
    else:
        _maybe_cache_specification(specification)
        X, y, _ = parse_dataset(
            _derive_path_from_specification(specification=specification), specification
        )
        return X, y


def to_TSDataLoaders(
    X_train: pandas.DataFrame,
    X_test: pandas.DataFrame,
    stride,
    window_length,
    batch_size,
    device,
    Y_train: pandas.DataFrame = None,
    Y_test: pandas.DataFrame = None,
):
    dsets = None
    if Y_train is None:
        dsets = TSDatasets(
            np.float32(slide_window_view(X_train, window_length, stride=stride)),
            np.float32(slide_window_view(X_train, window_length, stride=stride)),
        )
    else:
        dsets = TSDatasets(
            np.float32(slide_window_view(X_train, window_length, stride=stride)),
            np.float32(slide_window_view(Y_train, window_length, stride=stride)[:, -1]),
        )

    dls = TSDataLoaders.from_dsets(
        dsets.train, dsets.valid, bs=batch_size, num_workers=0, device=device
    )

    if X_test is None or X_test.shape[0] == 0:
        test_dls = None
    else:
        if Y_test is None:
            test_dsets = TSDatasets(
                np.float32(slide_window_view(X_test, window_length, stride=stride)),
                np.float32(slide_window_view(X_test, window_length, stride=stride)),
            )
        else:
            test_dsets = TSDatasets(
                np.float32(slide_window_view(X_test, window_length, stride=stride)),
                np.float32(
                    slide_window_view(Y_test, window_length, stride=stride)[:, -1]
                ),
            )

        test_dls = TSDataLoaders.from_dsets(
            test_dsets.train,
            test_dsets.valid,
            bs=batch_size,
            num_workers=0,
            device=device,
        )

    return dls, test_dls


if __name__ == "__main__":
    X, y = get_specification_as_pandas_dataframes(EF42_TEST_SYN_V2_18)
    print(str(X.head(50)))
    print(str(y))

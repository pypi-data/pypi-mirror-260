import numpy as np
import pandas
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def impute_missing_linear(data: pandas.DataFrame):
    columns = data.copy().columns
    data = fill_na_columns_with_zeros(data)
    imputer = IterativeImputer(missing_values=np.nan)
    imputer.fit(data)
    df = pandas.DataFrame(imputer.transform(data), columns=columns)
    df = df.interpolate(method="bfill", axis=0)
    return df, imputer


def fill_na_columns_with_zeros(df: pandas.DataFrame):
    df = df.copy()
    for col in df.columns:
        if df[col].isnull().all():
            df[col].fillna(0, inplace=True)
    return df

def normalize_z_score(data, mean, std):
    return (data - mean) / std


def get_na_columns(data):
    return [col for col in data.columns if data.loc[:, col].isna().any()]


def drop_na_columns_four(X_train: pandas.DataFrame, Y_train: pandas.DataFrame, X_test: pandas.DataFrame, Y_test: pandas.DataFrame):
    X_na_columns = get_na_columns(X_train)
    X_na_columns.extend(get_na_columns(X_test))
    X_na_columns = np.unique(X_na_columns)
    X_train = X_train.copy().drop(X_na_columns, inplace=False, axis=1, errors='ignore')
    X_test = X_test.copy().drop(X_na_columns, inplace=False, axis=1, errors='ignore')
    return X_train, Y_train, X_test, Y_test, X_na_columns


def drop_na_columns_two(X, Y):
    X_na_columns = get_na_columns(X)
    X = X.copy().drop(X_na_columns, inplace=False, axis=1, errors='ignore')
    return X, Y, X_na_columns

def normalization(X_train: pandas.DataFrame, X_test: pandas.DataFrame, normalization_method=normalize_z_score):
    X_train_means = X_train.mean(axis=0).values
    X_train_stds = X_train.std(axis=0).values
    X_train = normalization_method(X_train, X_train_means, X_train_stds)
    X_test = normalization_method(X_test, X_train_means, X_train_stds)
    return X_train, X_test, X_train_means, X_train_stds
    

def normalization_with_train_parameters(X_test, X_train_means, X_train_stds, normalization_method=normalize_z_score):
    return normalization_method(X_test, X_train_means, X_train_stds)


def preprocess(
    X_train: pandas.DataFrame, Y_train: pandas.DataFrame,
    X_test: pandas.DataFrame, Y_test: pandas.DataFrame,
    normalization_method=normalize_z_score
):
    X_train, imputer = impute_missing_linear(X_train)

    if not X_test.empty:
        columns = X_test.columns
        X_test = pandas.DataFrame(imputer.transform(X_test), columns=columns)

    if normalization_method:
        X_train, X_test, X_train_means, X_train_stds = normalization(X_train, X_test, normalization_method)

    X_train, Y_train, X_test, Y_test, dropped_columns = drop_na_columns_four(X_train, Y_train, X_test, Y_test)

    return X_train, Y_train, X_test, Y_test, imputer, dropped_columns, X_train_means, X_train_stds

def preprocess_anoformer(
    X_train: pandas.DataFrame, Y_train: pandas.DataFrame,
    X_test: pandas.DataFrame, Y_test: pandas.DataFrame,
    K: int,
):
    X_train, imputer = impute_missing_linear(X_train)

    if not X_test.empty:
        columns = X_test.columns
        X_test = pandas.DataFrame(imputer.transform(X_test), columns=columns)

    X_train, Y_train, X_test, Y_test, dropped_columns = drop_na_columns_four(X_train, Y_train, X_test, Y_test)

    x_min = X_train.min()
    x_max = X_train.max()

    # if 0 std, divide with (max - min) is nan, so make it 1
    maxmin = x_max - x_min
    maxmin[maxmin == 0] = 1

    X_train = (X_train - x_min) / maxmin
    X_train = X_train * (K-1)
    X_train = X_train.round(0)
    
    X_test = (X_test - x_min) / maxmin
    X_test = X_test * (K-1)
    X_test = X_test.round(0)

    X_test[X_test < 0] = 0
    X_test[X_test > K-1] = K-1

    return X_train, Y_train, X_test, Y_test, imputer, dropped_columns, x_min, x_max

def preprocess_with_imputer_and_fixed_normalization_parameters(X: pandas.DataFrame, Y: pandas.DataFrame, imputer: IterativeImputer, dropped_columns, X_train_means, X_train_stds, normalization_method=normalize_z_score):
    if not X.empty:
        columns = X.columns
        X = pandas.DataFrame(imputer.transform(X), columns=columns)

    X = normalization_with_train_parameters(X, X_train_means, X_train_stds)

    X = X.copy().drop(dropped_columns, inplace=False, axis=1, errors='ignore')

    X = X.interpolate(method="bfill", axis=0)

    return X, Y

def preprocess_with_imputer_and_fixed_normalization_parameters_anoformer(X: pandas.DataFrame, Y: pandas.DataFrame, imputer: IterativeImputer, dropped_columns, X_min, X_max, K):
    if not X.empty:
        columns = X.columns
        X = pandas.DataFrame(imputer.transform(X), columns=columns)

    X = X.copy().drop(dropped_columns, inplace=False, axis=1, errors='ignore')

    # if 0 std, divide with (max - min) is nan, so make it 1
    maxmin = X_max - X_min
    maxmin[maxmin == 0] = 1
  
    X = (X - X_min) / maxmin
    X = X * (K-1)
    X = X.round(0)

    X[X < 0] = 0
    X[X > K-1] = K-1

    return X, Y
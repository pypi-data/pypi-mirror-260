from torch.utils.data import Dataset
import numpy as np
import pandas as pd


class WindowedDataset(Dataset):
    def __init__(
        self,
        serial_data: pd.DataFrame,
        window_len: int,
        stride: int,
        transform=None,
        target_transform=None,
        label_col: str = "label",
        start_next_day: bool = True,
        time_col: str = "Time",
    ):
        self.transform = transform
        self.target_transform = target_transform
        self.label_col = label_col

        _windows_view = self._window_data(
            serial_data, window_len, stride, start_next_day, time_col
        )
        # copy the data as PyTorch does not support non-writable tensors
        # and for stride < window_len source data may be used multiple times
        self.windows = _windows_view[:, :-1].astype(np.float32, copy=True)
        self.labels = _windows_view[:, -1].astype(np.float32, copy=True)

    def _window_data(
        self,
        data_series: pd.DataFrame,
        window_len: int,
        stride: int,
        start_next_day: bool,
        time_col: str = "Time",
    ):
        _df = data_series.set_index(time_col) if time_col is not None else data_series
        if start_next_day:
            try:
                _ts = _df.index[0]
                _map_next_day = _df.index >= _ts.ceil(freq="D")
                _df = _df.loc[_map_next_day, :]

                _ts_begin = _df.index[0]
                if _ts_begin.ceil(freq="D") != _ts_begin:
                    print(
                        f"Warning: Starting at next day failed. Time of first time stamp is {_ts_begin.strftime('%X')}, expected '00:00:00'. Likely this is caused by missing data."
                    )
            except KeyError:
                print(
                    f"Warning: DataFrame does not contain column `{time_col}`. Unable to start windowing at next full day."
                )

        # ensure labels are in the last column
        if _df.columns[-1] != self.label_col:
            _df = _df.reindex(
                columns=_df.columns[_df.columns != self.label_col].to_list()
                + [self.label_col]
            )

        return np.lib.stride_tricks.sliding_window_view(_df, window_len, axis=0)[
            ::stride, :
        ]

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, index):
        _window = self.windows[index]
        _label = self.labels[index]

        if self.transform:
            _window = self.transform(_window)
        if self.target_transform:
            _label = self.target_transform(_label)

        return _window, _label

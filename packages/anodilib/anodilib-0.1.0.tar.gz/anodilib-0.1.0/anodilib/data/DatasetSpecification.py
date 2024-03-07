from typing import Callable, Tuple

import pandas as pd

class DatasetSpecification:
    """
    A class used to represent a Dataset and its parsing functionality

    Attributes
    ----------
    dataset_name : str
        the name of the dataset (can be used to load this dataset)
    location : str
        the location of the dataset, can be either an url to location where the dataset can be directly downloaded (e.g. nextcloud download link)
        or a path (which one is automatically detected); if None it will be derived from dataset_name
    delimiter : str
        how the features values are splitted in each line
    label_column : int
        the index of the label column
    is_data_column : Callable[[int], bool]
        a mapping from a columns index to whether this column is one of the data columns which should be used
    columns : list[str]
        a list of column names which are used when using parquet as file type
    skip_header : int
        how many header columns to skip
    skip_footer : int
        how many footer columns to skip
    label_realizations : Tuple[str, str]
        the type of labels for OK (no anomaly) and NOK (anomaly) in the format (OK, NOK); e.g. ("-1", "1") if -1 is no anomaly and 1 is anomaly
    decimal : str
        character for decimal point
    only_first_n_entries : int
        limits the items of the dataset to the first n entries
    predefined_dataset : Tuple[pd.Dataframe, pd.Dataframe]
        the dataset if it should not use the parsing framework (in case the datasets format cannot be captured by the mechanisms)
    """

    def __init__(
        self,
        dataset_name: str,
        location: str,
        delimiter: str,
        label_column: int,
        is_data_column: Callable[[int], bool],
        columns: list[str] = None,
        skip_header: int = 1,
        skip_footer: int = 0,
        label_realizations: Tuple[str, str] = (0, 1),
        decimal: str = ".",
        only_first_n_entries: int = -1,
        predefined_dataset: Tuple[pd.DataFrame, pd.DataFrame] = None,
    ):
        self.dataset_name = dataset_name
        self.location = location
        self.delimiter = delimiter
        self.label_column = label_column
        self.is_data_column = is_data_column
        self.columns = columns
        self.skip_header = skip_header
        self.skip_footer = skip_footer
        self.label_realizations = label_realizations
        self.decimal = decimal
        self.only_first_n_entries = only_first_n_entries
        self.predefined_dataset = predefined_dataset


EF42_TRAIN = DatasetSpecification(
    dataset_name="EF42_train.parquet",
    location=None,
    delimiter=None,
    label_column=7,
    is_data_column=lambda c: c < 7,
    columns=[
        "6_CN33 11 01 01_WTarif1",
        "6_CN33 11 01 01_Dfluss",
        "6_CN33 21 01 01_Dfluss",
        "6_CN33 21 01 01_Wleistung",
        "1_CN33 71 02 03_WV+T1",
        "1_CN33 71 02 03_BV+T1",
        "Dayofweek",
        "label",
    ],
    skip_header=1,
    skip_footer=0,
    label_realizations=[0, 1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
ECG200_TRAIN = DatasetSpecification(
    dataset_name="ECG200_TRAIN.txt",
    location="https://cloud.fachschaften.org/s/czR7BBLtkrjL8bM/download/ECG200_TRAIN.txt",
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
ECG200_TEST = DatasetSpecification(
    dataset_name="ECG200_TEST.txt",
    location="https://cloud.fachschaften.org/s/qR4tc9GsnLG2Qk3/download/ECG200_TEST.txt",
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
WADI = DatasetSpecification(
    dataset_name="WADI.A2_19_Nov_2019_WADI_attackdataLABLE.csv",
    location="https://cloud.fachschaften.org/s/mL6XKsa8aQEpGDz/download/WADI.A2_19_Nov_2019_WADI_attackdataLABLE.csv",
    delimiter=",",
    label_column=130,
    is_data_column=lambda c: c != 130 and c >= 3,
    columns=None,
    skip_header=3,
    skip_footer=3,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
SWAT = DatasetSpecification(
    "SWaT_dataset_Jul_19_v2_labeled.csv",
    location="https://cloud.fachschaften.org/s/2ooDNFtLWnBGzao/download/SWaT_dataset_Jul_19_v2_labeled.csv",
    delimiter=";",
    label_column=83,
    is_data_column=lambda c: c > 0 and c != 83,
    columns=None,
    skip_header=3,
    skip_footer=71,
    label_realizations=[0, 1],
    decimal=",",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
ECG_5D_TEST = DatasetSpecification(
    "ECGFiveDays_TEST.txt",
    location=None,
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, 2],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
ECG_5D_TRAIN = DatasetSpecification(
    "ECGFiveDays_TRAIN.txt",
    location=None,
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, 2],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
WAFER_TEST = DatasetSpecification(
    "Wafer_TEST.txt",
    location="https://cloud.fachschaften.org/s/qoesLK798LeWeWY/download/Wafer_TEST.txt",
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
WAFER_TRAIN = DatasetSpecification(
    "Wafer_TRAIN.txt",
    location="https://cloud.fachschaften.org/s/nP9yyPpHcLot79z/download/Wafer_TRAIN.txt",
    delimiter="  ",
    label_column=0,
    is_data_column=lambda c: c != 0,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
IOT_CTU_MALWARE_CAPTURE = DatasetSpecification(
    "IoT-CTU-IoT-Malware-Capture-3-1",
    # IoT\opt\Malware-Project\BigDataset\IoTScenarios\CTU-IoT-Malware-Capture-3-1\bro\conn.log.labeled (hat so 156000 Zeilen)
    location="https://cloud.fachschaften.org/s/4cFf3KwscyQkTjt/download/conn.log.labeled",
    delimiter="	",
    label_column=21,
    is_data_column=lambda c: c > 0 and c != 21,
    columns=None,
    skip_header=8,
    skip_footer=1,
    label_realizations=["Benign", "Malicious"],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
IOT23_SMALL_LABELED = DatasetSpecification(
    "IoT23_small_dataset_labeled.txt",
    location="https://cloud.fachschaften.org/s/K86T9NyzwDojapa/download/IoT23_small_dataset_labeled.txt",
    delimiter="	",
    label_column=21,
    is_data_column=lambda c: c > 0 and c != 21,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=["Benign", "Malicious"],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
IOT23_SMALL_LABELED_2 = DatasetSpecification(
    "IoT23_small_data_labeled2.txt",
    location="https://cloud.fachschaften.org/s/dP8DpbZEDTnLZ5G/download/IoT23_small_data_labeled2.txt",
    delimiter="	",
    label_column=21,
    is_data_column=lambda c: c > 0 and c != 21,
    columns=None,
    skip_header=0,
    skip_footer=0,
    label_realizations=["Benign", "Malicious"],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
EF42_TEST_SYN_V2_18 = DatasetSpecification(
    "EF42_test_syn_v2_18.parquet",
    location=None,
    delimiter=None,
    label_column=7,
    is_data_column=lambda c: c < 7,
    columns=[
        "6_CN33 11 01 01_WTarif1",
        "6_CN33 11 01 01_Dfluss",
        "6_CN33 21 01 01_Dfluss",
        "6_CN33 21 01 01_Wleistung",
        "1_CN33 71 02 03_WV+T1",
        "1_CN33 71 02 03_BV+T1",
        "Dayofweek",
        "label",
    ],
    skip_header=1,
    skip_footer=0,
    label_realizations=[0, 1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)
EF42_TEST_SYN_V2_18_FEAT_LBL = DatasetSpecification(
    "EF42_test_syn_v2_18_feat_lbl.parquet",
    location=None,
    delimiter=None,
    label_column=0,
    is_data_column=lambda c: c > 0,
    columns=[
        "label",
        "label_real",
        "label_syn",
    ],
    skip_header=1,
    skip_footer=0,
    label_realizations=[0, 1],
    decimal=".",
    only_first_n_entries=-1,
    predefined_dataset=None,
)

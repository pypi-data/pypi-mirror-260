# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.ModifiedLSTM import ModifiedLSTM

from data.DatasetSpecification import ECG200_TRAIN, ECG200_TEST
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *


_batch_size = 28
_window_length = 4
_stride = 1

# wadi = DATASETS["SWaT_dataset_Jul_19_v2_labeled"]
# wadi = DATASETS["WADI.A2_19_Nov_2019_WADI_attackdataLABLE"]
# wadi = DATASETS["ECGFiveDays_TEST"]
# wadi = DATASETS["_syn.parquet"]
# train = DATASETS["IoT23_small_data_labeled2"]
# test = DATASETS["IoT23_small_data_labeled2"]
train = ECG200_TRAIN
test = ECG200_TEST

alg = ModifiedLSTM(
    dataset_specification=train,
    batch_size=_batch_size,
    window_len=_window_length,
    stride=_stride,
)
alg.fit(epoch_num=50, learning_rate="lr_find", learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find", learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find", learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find", learning_rate_iteration=200)
alg.predict(dataset_specification=test)
anoms, df_error_norms_testing, final_anomaly_threshold = alg.getAnomalies()

labels_translated = np.array(alg.Y_test_df)

adjusted_labels = adjust_points_smoothing(anoms, labels_translated)

print("adjusted", c_f1_score(adjusted_labels, labels_translated))
print("original", c_f1_score(anoms, labels_translated))

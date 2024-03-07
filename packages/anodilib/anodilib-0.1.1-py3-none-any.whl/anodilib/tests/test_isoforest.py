# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.IsolationForest import IsolationForest as IF

from data.DatasetSpecification import WADI
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *

# train = DATASETS["ECG200_TRAIN"]
# test = DATASETS["ECG200_TEST"]
# train = DATASETS["EF42_train.parquet"]
train = WADI

alg = IF(dataset_specification=train, contamination="auto", test_fraction=0.2)
alg.fit()
alg.predict()
anoms = alg.getAnomalies()

labels_translated = np.array(alg.Y_test_df)

adjusted_labels = adjust_points_smoothing(anoms, labels_translated)

print("adjusted", c_f1_score(adjusted_labels, labels_translated))
print("original", c_f1_score(anoms, labels_translated))

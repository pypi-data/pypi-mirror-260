# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.TranVAE import TranVAE

from data.DatasetSpecification import WADI
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *

wadi = WADI
_batch_size = 28
_window_length = 96

alg = TranVAE(dataset_specification=wadi, 
              window_length=_window_length,
              num_layers=1,
              batch_size=_batch_size)
alg.fit(epoch_num=1)
alg.predict()
anoms, df_error_norms_testing, final_anomaly_threshold = alg.getAnomalies()

labels_translated = np.array(alg.Y_test_df)

adjusted_labels = adjust_points_smoothing(anoms[0], labels_translated)

print("adjusted", c_f1_score(adjusted_labels, labels_translated))
print("original", c_f1_score(anoms[0], labels_translated))

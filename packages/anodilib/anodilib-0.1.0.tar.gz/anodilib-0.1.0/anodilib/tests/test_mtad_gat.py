# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.MTAD_GAT import MTAD_GAT

from data.DatasetSpecification import WAFER_TEST, WAFER_TRAIN
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *

data = WAFER_TRAIN

_batch_size = 28
_window_length = 96
_learning_rate = 1e-3

alg = MTAD_GAT(dataset_specification=data, 
               batch_size=_batch_size, 
               window_length=_window_length,
               learning_rate=_learning_rate,
               L=1,
               verbose=True,
               dynamic_pot=True,
               level=0.6)
alg.fit(epoch_num=2)
alg.predict(WAFER_TEST)
preds, _, _ = alg.getAnomalies()

anoms = preds[0]
labels_translated = np.array(alg.Y_test_df)

adjusted_labels = adjust_points_smoothing(anoms, labels_translated)

print("adjusted", c_f1_score(adjusted_labels, labels_translated))
print("original", c_f1_score(anoms, labels_translated))

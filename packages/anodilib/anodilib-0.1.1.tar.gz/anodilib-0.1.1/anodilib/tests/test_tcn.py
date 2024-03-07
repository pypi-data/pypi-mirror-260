# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.TCNAE import TCNAE
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *
import numpy as np
from data.DatasetSpecification import WADI


alg = TCNAE(WADI,
            latent_features=4,
            kernel_size=8,
            pool_size=32,
            dropout=0.2,
            num_channels=[32] * 5,
            batch_size=64,
            window_len=96,
            stride=96)

alg.fit(epoch_num=1)
alg.predict()
anoms, _, _ = alg.getAnomalies()
print(anoms)

adjusted_labels = adjust_points_smoothing(anoms, alg.Y_test_df.values)

print("adjusted", c_f1_score(adjusted_labels, np.array(alg.Y_test_df.values)))
print("original", c_f1_score(anoms, np.array(alg.Y_test_df.values)))

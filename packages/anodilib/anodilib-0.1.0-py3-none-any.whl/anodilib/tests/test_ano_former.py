# state-of-the-art fashion for being able to import from other directories
import os
import sys

# for M1 Processor!!!
# os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.AnoFormer import AnoFormer

from data.DatasetSpecification import EF42_TRAIN, EF42_TEST_SYN_V2_18
from metrics.pa.pointAdjustment import *
from metrics.cmetrics import *

import torch

data = EF42_TRAIN

_batch_size = 28
_window_length = 96 #in anoformer the layer-sizes are dependent from window length * features, 96*152 in wafer = 15000 -> too big for gpu
_learning_rate = 1e-2

alg = AnoFormer(dataset_specification=data, 
                batch_size=_batch_size, 
                window_len=_window_length,
                learning_rate=_learning_rate,
                n_critic = 0,
                d=50,
                substitute_value = lambda x: 100,
                lambda_adv=0,
                verbose=False,
                device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
                L=3, critic_L=0,
                K=200,
                stride=1
                )

alg.fit(epoch_num=2)
alg.predict(EF42_TEST_SYN_V2_18)
preds, _= alg.getAnomalies(quantile=0.8)

labels_translated = np.array(alg.Y_test_df)

adjusted_labels = adjust_points_smoothing(preds, labels_translated)

print("adjusted", c_f1_score(adjusted_labels, labels_translated))
print("original", c_f1_score(preds, labels_translated))

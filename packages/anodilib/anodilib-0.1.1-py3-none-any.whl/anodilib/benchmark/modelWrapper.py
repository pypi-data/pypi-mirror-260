import os
import sys
from dataclasses import dataclass
from typing import Callable, TypeVar

from paramSet import ParamSet

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from algorithm.algorithm import Algorithm

A = TypeVar("A", bound=Algorithm)
P = TypeVar("P", bound=ParamSet)


@dataclass
class EpochRange:
    interval: int
    count: int

    def getRange(self) -> range:
        return range(self.interval, self.interval * self.count + 1, self.interval)

    def __call__(self, datasetId):
        return self


@dataclass
class ModelWrapper:
    modelClass: type[A]
    fit: Callable[[A, int], None]
    getAnomalies: Callable[[A], list[bool | float]]
    psEpochRange: Callable[[str], EpochRange]
    bmEpochRange: Callable[[str], EpochRange]
    getPSParams: Callable[[str], list[list[P]]]
    getBMParams: Callable[[str], list[list[P]]] = None
    applyPSAnomalyParam: Callable[[A, P], None] = None
    getPredErrors: Callable[[A], list[float | list[float]]] = lambda _: None

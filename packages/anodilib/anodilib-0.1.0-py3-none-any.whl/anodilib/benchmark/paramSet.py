from dataclasses import dataclass, asdict
from typing import Callable


@dataclass
class ParamSet:
    def asdict(self):
        return asdict(self)

    def toString(self):
        return str(self.asdict())

    def toFilenameString(self):
        return self.toString().replace("'", "").replace(": ", "=").replace(":", "").replace(".", "")


@dataclass
class AnoFormerParams(ParamSet):
    K: int
    d: int
    dim_feedforward: int
    substitute_value: Callable
    anomaly_quantile: float
    L: int
    window_len: int

    def toString(self):
        dict = super().asdict()
        dict["substitute_value"] = dict["substitute_value"].__name__
        return str(dict)


@dataclass
class MLSTMParams(ParamSet):
    hidden_size: int
    number_layers: int
    thresh_stepsize: float
    clusterselection: int
    window_len: int
    pruning: bool
    p: float
    t_delta: int


@dataclass
class MTAD_GATParams(ParamSet):
    gamma: float
    recon_latent_dim: int
    window_length: int


@dataclass
class TranVAEParams(ParamSet):
    num_layers: int
    kld_weight: float
    window_length: int


@dataclass
class EmptyParams(ParamSet):
    pass


@dataclass
class RandomParams(ParamSet):
    p_anom: float

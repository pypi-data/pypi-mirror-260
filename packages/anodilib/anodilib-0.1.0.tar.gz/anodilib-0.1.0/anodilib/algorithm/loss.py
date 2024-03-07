import torch
import math


# from "https://datascience.stackexchange.com/questions/96271/logcoshloss-on-pytorch"
def log_cosh_loss(y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
    def _log_cosh(x: torch.Tensor) -> torch.Tensor:
        return x + torch.nn.functional.softplus(-2.0 * x) - math.log(2.0)

    return torch.mean(_log_cosh(y_pred - y_true))


class LogCoshLoss(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        return log_cosh_loss(y_pred, y_true)


class DiffLoss(torch.nn.Module):
    def __init__(self, reduction=None):
        super().__init__()

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        return y_pred - y_true


class ELBOLoss(torch.nn.Module):
    def __init__(self, kld_weight: float = 0.5):
        self.kld_weight = kld_weight
        super(ELBOLoss, self).__init__()

    def forward(
        self,
        recons: torch.Tensor,
        mu: torch.Tensor,
        var: torch.Tensor,
        target: torch.Tensor,
        *args,
        **kwargs,
    ) -> torch.Tensor:
        # calculated as batch_size/sequence_size
        recons_loss = torch.nn.functional.mse_loss(recons, target, reduction="mean")
        kld_loss = -0.5 * torch.mean(1 + var - mu.pow(2) - var.exp())
        loss = recons_loss + self.kld_weight * kld_loss

        return loss

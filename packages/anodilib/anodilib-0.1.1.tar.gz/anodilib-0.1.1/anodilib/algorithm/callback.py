from fastai.data.all import Path
from fastai.learner import *
from fastai.callback.core import *
from fastai.data.all import *


class GatherPredsCallbackTCNAE(GatherPredsCallback):
    def __init__(
        self,
        reduce_loss=True,
        with_input: bool = False,
        with_loss: bool = False,
        save_preds: Path = None,
        save_targs: Path = None,
        with_preds: bool = True,
        with_targs: bool = True,
        concat_dim: int = 0,
        pickle_protocol: int = 2,
    ):
        super().__init__(
            with_input,
            with_loss,
            save_preds,
            save_targs,
            with_preds,
            with_targs,
            concat_dim,
            pickle_protocol,
        )

        self.reduce_loss = reduce_loss

    def after_batch(self):
        "Save predictions, targets and potentially losses"
        if not hasattr(self, "pred"):
            return
        preds, targs = self.learn.to_detach(self.pred), self.learn.to_detach(self.yb)
        if self.with_preds:
            self.preds.append(preds)
        if self.with_targs:
            self.targets.append(targs)
        if self.save_preds is not None:
            torch.save(
                preds,
                self.save_preds / str(self.iter),
                pickle_protocol=self.pickle_protocol,
            )
        if self.save_targs is not None:
            torch.save(
                targs[0],
                self.save_targs / str(self.iter),
                pickle_protocol=self.pickle_protocol,
            )
        if self.with_loss:
            bs = find_bs(self.yb)
            loss = (
                self.loss
                if self.loss.numel() == bs or not self.reduce_loss
                else self.loss.view(bs, -1).mean(1)
            )
            self.losses.append(self.learn.to_detach(loss))


class GatherPredsCallbackLSTM(GatherPredsCallback):
    def __init__(self, reduce_loss=True, with_input: bool = False, with_loss: bool = False, save_preds: Path = None, save_targs: Path = None, with_preds: bool = True, with_targs: bool = True, concat_dim: int = 0, pickle_protocol: int = 2):
        super().__init__(with_input, with_loss, save_preds, save_targs, with_preds, with_targs, concat_dim, pickle_protocol)

        self.reduce_loss = reduce_loss

    def after_batch(self):
        "Save predictions, targets and potentially losses"
        if not hasattr(self, 'pred'): 
            return
        preds, targs = self.learn.to_detach(self.pred), self.learn.to_detach(self.yb)
        if self.with_preds: 
            self.preds.append(preds)
        if self.with_targs: 
            self.targets.append(targs)
        if self.save_preds is not None: 
            torch.save(preds, self.save_preds / str(self.iter), pickle_protocol=self.pickle_protocol)
        if self.save_targs is not None: 
            torch.save(targs[0], self.save_targs / str(self.iter), pickle_protocol=self.pickle_protocol)
        if self.with_loss:
            bs = find_bs(self.yb)
            loss = self.loss if self.loss.numel() == bs or not self.reduce_loss else self.loss.view(bs, -1).mean(1)
            self.losses.append(self.learn.to_detach(loss))


class LSTMPredCallback(Callback):
    def before_batch(self):
        self.tmp_xb = self.xb[0]
        self.learn.xb = (self.xb[0][:, :-1, :],)
        self.learn.yb = (self.tmp_xb[:, -1, :],)

    def after_pred(self):
        self.learn.pred = self.pred[:, -1, :]
        self.learn.yb = (self.tmp_xb[:, -1, :],)


class MTAD_GATFitCallback(Callback):
    """
    cuts window_length+1 long window to :window_length as x and -1 as y for forecaster
    """
    def before_batch(self):
        self.learn.yb = (self.xb[0][:, :, -1],)
        self.learn.xb = (self.xb[0][:, :, :-1].permute(0, 2, 1),)


class GatherPredsCallbackTranVAE(GatherPredsCallback):
    def __init__(
        self,
        reduce_loss=True,
        with_input: bool = False,
        with_loss: bool = False,
        save_preds: Path = None,
        save_targs: Path = None,
        with_preds: bool = True,
        with_targs: bool = True,
        concat_dim: int = 0,
        pickle_protocol: int = 2,
    ):
        super().__init__(
            with_input,
            with_loss,
            save_preds,
            save_targs,
            with_preds,
            with_targs,
            concat_dim,
            pickle_protocol,
        )

        self.reduce_loss = reduce_loss

    def all_tensors(self) -> (Tensor, list):
        "Returns all recorded tensors in the order [inputs, preds, targets, losses]"
        res = [
            self.preds if self.with_preds else None,
            self.targets if self.with_targs else None,
        ]
        if self.with_input:
            res = [self.inputs] + res
        if self.with_loss:
            res.append(self.losses)
        return res


class SwapSequenceChannelCallbackTranVae(Callback):
    def before_batch(self):
        self.learn.xb = (self.xb[0].permute(0, 2, 1),)


class SwapSequenceChannelCallbackAnoFormer(Callback):
    def before_batch(self):
        self.learn.xb = (self.xb[0].permute(0, 2, 1),)
        self.learn.yb = (self.yb[0].permute(0, 2, 1),)

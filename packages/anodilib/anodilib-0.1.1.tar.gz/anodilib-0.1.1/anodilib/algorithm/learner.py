from typing import MutableSequence
from fastai.data.all import delegates, L
from fastai.learner import Learner, _ConstantFunc
from fastai.callback.core import DataLoaders, Callback, DataLoader, GatherPredsCallback
from fastai.torch_core import nested_reorder
from fastcore.xtras import ContextManagers
from fastcore.basics import getcallable
from torch import tensor
from fastai.learner import *
from fastai.callback.core import *
from fastai.data.all import *

# custom imports
from algorithm.callback import GatherPredsCallbackTCNAE, GatherPredsCallbackTranVAE, GatherPredsCallbackLSTM


class TCNAELearner(Learner):
    def __init__(self, dls: DataLoaders, model: callable, *args, **kwargs):
        super().__init__(dls, model, *args, **kwargs)

    @delegates(GatherPredsCallback.__init__)
    def get_preds(
        self,
        ds_idx: int = 1,  # `DataLoader` to use for predictions if `dl` is None. 0: train. 1: valid
        dl=None,  # `DataLoader` to use for predictions, defaults to `ds_idx=1` if None
        with_input: bool = False,  # Return inputs with predictions
        with_decoded: bool = False,  # Return decoded predictions
        with_loss: bool = False,  # Return per item loss with predictions
        act=None,  # Apply activation to predictions, defaults to `self.loss_func`'s activation
        inner: bool = False,  # If False, create progress bar, show logger, use temporary `cbs`
        reorder: bool = True,  # Reorder predictions on dataset indicies, if applicable
        cbs: Callback
        | MutableSequence
        | None = None,  # Temporary `Callback`s to apply during prediction
        **kwargs,
    ) -> tuple:
        if dl is None:
            dl = self.dls[ds_idx].new(shuffle=False, drop_last=False)
        else:
            try:
                len(dl)
            except TypeError:
                raise TypeError(f"`dl` is {type(dl)} and doesn't have len(dl)")
        if isinstance(dl, DataLoader):
            if dl.drop_last:
                dl = dl.new(shuffle=False, drop_last=False)
        if reorder and hasattr(dl, "get_idxs"):
            idxs = dl.get_idxs()
            dl = dl.new(get_idxs=_ConstantFunc(idxs))
        cb = GatherPredsCallbackTCNAE(
            reduce_loss=False, with_input=with_input, with_loss=with_loss, **kwargs
        )
        ctx_mgrs = self.validation_context(cbs=L(cbs) + [cb], inner=inner)
        if with_loss:
            ctx_mgrs.append(self.loss_not_reduced())
        with ContextManagers(ctx_mgrs):
            self._do_epoch_validate(dl=dl)
            if act is None:
                act = getcallable(self.loss_func, "activation")
            res = cb.all_tensors()
            pred_i = 1 if with_input else 0
            if res[pred_i] is not None:
                res[pred_i] = act(res[pred_i])
                if with_decoded:
                    res.insert(
                        pred_i + 2, getcallable(self.loss_func, "decodes")(res[pred_i])
                    )
            if reorder and hasattr(dl, "get_idxs"):
                res = nested_reorder(res, tensor(idxs).argsort())
            return tuple(res)
        self._end_cleanup()


class LSTMLearner(Learner):
    def __init__(self, dls: DataLoaders, model: callable, *args, **kwargs):
        super().__init__(dls, model, *args, **kwargs)

    @delegates(GatherPredsCallback.__init__)
    def get_preds(
        self, 
        ds_idx: int = 1,  # `DataLoader` to use for predictions if `dl` is None. 0: train. 1: valid
        dl=None,  # `DataLoader` to use for predictions, defaults to `ds_idx=1` if None
        with_input: bool = False,  # Return inputs with predictions
        with_decoded: bool = False,  # Return decoded predictions
        with_loss: bool = False,  # Return per item loss with predictions
        act=None,  # Apply activation to predictions, defaults to `self.loss_func`'s activation
        inner: bool = False,  # If False, create progress bar, show logger, use temporary `cbs`
        reorder: bool = True,  # Reorder predictions on dataset indicies, if applicable
        cbs: Callback | MutableSequence | None = None,  # Temporary `Callback`s to apply during prediction
        **kwargs
    ) -> tuple:
        if dl is None: 
            dl = self.dls[ds_idx].new(shuffle=False, drop_last=False)
        else:
            try: 
                len(dl)
            except TypeError:
                raise TypeError(f"`dl` is {type(dl)} and doesn't have len(dl)")
        if isinstance(dl, DataLoader):
            if dl.drop_last: 
                dl = dl.new(shuffle=False, drop_last=False)
        if reorder and hasattr(dl, 'get_idxs'):
            idxs = dl.get_idxs()
            dl = dl.new(get_idxs=_ConstantFunc(idxs))
        cb = GatherPredsCallbackLSTM(reduce_loss=False, with_input=with_input, with_loss=with_loss, **kwargs)
        ctx_mgrs = self.validation_context(cbs=L(cbs) + [cb], inner=inner)
        if with_loss: 
            ctx_mgrs.append(self.loss_not_reduced())
        with ContextManagers(ctx_mgrs):
            self._do_epoch_validate(dl=dl)
            if act is None: 
                act = getcallable(self.loss_func, 'activation')
            res = cb.all_tensors()
            pred_i = 1 if with_input else 0
            if res[pred_i] is not None:
                res[pred_i] = act(res[pred_i])
                if with_decoded:
                    res.insert(pred_i + 2, getcallable(self.loss_func, 'decodes')(res[pred_i]))
            if reorder and hasattr(dl, 'get_idxs'): 
                res = nested_reorder(res, tensor(idxs).argsort())
            return tuple(res)
        self._end_cleanup()


class TranVAELearner(Learner):
    def __init__(self, dls: DataLoaders, model: callable, *args, **kwargs):
        super().__init__(dls, model, *args, **kwargs)

    @delegates(GatherPredsCallbackTranVAE.__init__)
    def get_preds(
        self,
        ds_idx: int = 1,  # `DataLoader` to use for predictions if `dl` is None. 0: train. 1: valid
        dl=None,  # `DataLoader` to use for predictions, defaults to `ds_idx=1` if None
        with_input: bool = False,  # Return inputs with predictions
        with_decoded: bool = False,  # Return decoded predictions
        with_loss: bool = False,  # Return per item loss with predictions
        act=None,  # Apply activation to predictions, defaults to `self.loss_func`'s activation
        inner: bool = False,  # If False, create progress bar, show logger, use temporary `cbs`
        reorder: bool = True,  # Reorder predictions on dataset indicies, if applicable
        cbs: Callback
        | MutableSequence
        | None = None,  # Temporary `Callback`s to apply during prediction
        **kwargs,
    ) -> tuple:
        if dl is None:
            dl = self.dls[ds_idx].new(shuffle=False, drop_last=False)
        else:
            try:
                len(dl)
            except TypeError:
                raise TypeError(f"`dl` is {type(dl)} and doesn't have len(dl)")
        if isinstance(dl, DataLoader):
            if dl.drop_last:
                dl = dl.new(shuffle=False, drop_last=False)
        if reorder and hasattr(dl, "get_idxs"):
            idxs = dl.get_idxs()
            dl = dl.new(get_idxs=_ConstantFunc(idxs))
        cb = GatherPredsCallbackTranVAE(
            reduce_loss=False, with_input=with_input, with_loss=with_loss, **kwargs
        )
        ctx_mgrs = self.validation_context(cbs=L(cbs) + [cb], inner=inner)
        if with_loss:
            ctx_mgrs.append(self.loss_not_reduced())
        with ContextManagers(ctx_mgrs):
            self._do_epoch_validate(dl=dl)
            res = cb.all_tensors()
            if reorder and hasattr(dl, "get_idxs"):
                res = nested_reorder(res, tensor(idxs).argsort())
            return tuple(res)
        self._end_cleanup()

    def _do_one_batch_validate(self):
        self.pred = self.model.get_score(*self.xb)
        self("after_pred")
        return

    def one_batch_validate(self, i, b):
        self.iter = i
        b = self._set_device(b)
        self._split(b)
        self._with_events(self._do_one_batch_validate, "batch", CancelBatchException)

    def all_batches_validate(self):
        self.n_iter = len(self.dl)
        for o in enumerate(self.dl):
            self.one_batch_validate(*o)

    def _do_epoch_validate(self, ds_idx=1, dl=None):
        if dl is None:
            dl = self.dls[ds_idx]
        self.dl = dl
        with torch.no_grad():
            self._with_events(
                self.all_batches_validate, "validate", CancelValidException
            )

    def _do_one_batch(self):
        self.pred, mu, var = self.model(*self.xb)
        self("after_pred")
        self.loss_grad = self.loss_func(self.pred, mu, var, *self.xb)
        self.loss = self.loss_grad.clone()
        self("after_loss")
        self._do_grad_opt()

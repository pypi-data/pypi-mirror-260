import torch
import torch.nn as nn
from torch.nn.init import _calculate_fan_in_and_fan_out
import math


def _no_grad_normal(tensor, mean, std, generator=None):
    with torch.no_grad():
        return tensor.normal_(mean, std, generator=generator)


def init_glorot_normal(tensor, gain: float = 1.0, generator=None):
    """Reimplementation of torch.nn.init.xavier_normal_ with generator arg"""

    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)
    std = gain * math.sqrt(2.0 / float(fan_in + fan_out))

    return _no_grad_normal(tensor, 0.0, std, generator=generator)

def pdf(data, mu, var):
  #var usually 1e-1 - 1e-2
  epsilon = 1e-14

  #p get sometimes 1e-42 (>max float32)
  #normal gaussian formula
  return torch.exp(-torch.pow(data - mu, 2) / (2.0 * (var + epsilon))) / torch.sqrt(2.0 * torch.pi * (var + epsilon))

class PositionalEmbedding(nn.Module):
    """inspired from https://github.com/codertimo/BERT-pytorch/blob/master/bert_pytorch/model/embedding/"""
    def __init__(self, d_model, max_len=512):
        super().__init__()

        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, d_model).float()
        pe.require_grad = False

        position = torch.arange(0, max_len).float().unsqueeze(1)
        div_term = (torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model)).exp()

        # Fix for uneven number of features
        pe[:, 0::2] = torch.sin(position * div_term[:math.ceil(d_model / 2)])
        pe[:, 1::2] = torch.cos(position * div_term[:math.floor(d_model / 2)])

        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return self.pe[:, :x.size(1)]


class BERTEmbedding(nn.Module):
    """
    inspired from https://github.com/codertimo/BERT-pytorch/blob/master/bert_pytorch/model/embedding/
    BERT Embedding which is consisted with under features
        1. TokenEmbedding : normal embedding matrix
        2. PositionalEmbedding : adding positional information using sin, cos

        sum of all these features are output of BERTEmbedding
    """

    def __init__(self, vocab_size, embed_size):
        """
        :param vocab_size: total vocab size
        :param embed_size: embedding size of token embedding
        :param dropout: dropout rate
        """
        super().__init__()
        self.token = TokenEmbedding(vocab_size=vocab_size, embed_size=embed_size)
        self.position = PositionalEmbedding(d_model=self.token.embedding_dim)
        self.embed_size = embed_size

    def forward(self, sequence): #formerly had unused segment_label
        x = self.token(sequence.type(torch.int32)) + self.position(sequence.type(torch.int32))[:, :, None,]
        return x


class TokenEmbedding(nn.Embedding):
    """inspired from https://github.com/codertimo/BERT-pytorch/blob/master/bert_pytorch/model/embedding/"""
    def __init__(self, vocab_size, embed_size=512):
        super().__init__(vocab_size, embed_size, padding_idx=0)

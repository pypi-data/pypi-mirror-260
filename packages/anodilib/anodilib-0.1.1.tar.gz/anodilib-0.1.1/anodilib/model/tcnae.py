import torch.nn as nn
from torch.nn.utils import weight_norm
from .utils import init_glorot_normal


class Chomp1d(nn.Module):
    def __init__(self, chomp_size):
        super(Chomp1d, self).__init__()
        self.chomp_size = chomp_size

    def forward(self, x):
        return x[:, :, : -self.chomp_size].contiguous()


class TemporalBlock(nn.Module):
    def __init__(
        self,
        n_inputs,
        n_outputs,
        kernel_size,
        stride,
        dilation,
        padding,
        dropout=0.2,
        generator=None,
        **kwargs
    ):
        super(TemporalBlock, self).__init__()
        self.activation = kwargs.get("activation", nn.ReLU)

        self.conv1 = weight_norm(
            nn.Conv1d(
                n_inputs,
                n_outputs,
                kernel_size,
                stride=stride,
                padding=padding,
                dilation=dilation,
            )
        )
        self.chomp1 = Chomp1d(padding)
        self.act1 = self.activation()
        self.dropout1 = nn.Dropout1d(dropout)

        self.conv2 = weight_norm(
            nn.Conv1d(
                n_outputs,
                n_outputs,
                kernel_size,
                stride=stride,
                padding=padding,
                dilation=dilation,
            )
        )
        self.chomp2 = Chomp1d(padding)
        self.act2 = self.activation()
        self.dropout2 = nn.Dropout1d(dropout)

        self.net = nn.Sequential(
            self.conv1,
            self.chomp1,
            self.act1,
            self.dropout1,
            self.conv2,
            self.chomp2,
            self.act2,
            self.dropout2,
        )
        self.downsample = (
            nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        )
        self.act = self.activation()
        self.init_weights(generator=generator)

    def init_weights(self, generator=None):
        init_glorot_normal(self.conv1.weight, generator=generator)
        init_glorot_normal(self.conv2.weight, generator=generator)
        if self.downsample is not None:
            init_glorot_normal(self.downsample.weight, generator=generator)

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.act(out + res)


class TemporalConvNet(nn.Module):
    def __init__(self, num_inputs, num_channels, kernel_size=2, dropout=0.2, **kwargs):
        super(TemporalConvNet, self).__init__()
        layers = []
        num_levels = len(num_channels)
        for i in range(num_levels):
            dilation_size = 2**i
            in_channels = num_inputs if i == 0 else num_channels[i - 1]
            out_channels = num_channels[i]
            layers += [
                TemporalBlock(
                    in_channels,
                    out_channels,
                    kernel_size,
                    stride=1,
                    dilation=dilation_size,
                    padding=(kernel_size - 1) * dilation_size,
                    dropout=dropout,
                    kwargs=kwargs,
                )
            ]

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


class TCNAE(nn.Module):
    def __init__(
        self,
        input_features: int,
        num_channels: list,
        latent_features: int,
        kernel_size: int,
        pool_size: int,
        dropout: float = 0.2,
        generator=None,
        **kwargs
    ):
        super().__init__()

        self.activation = kwargs.get("activation", nn.ReLU)

        self.encoder = nn.Sequential(
            TemporalConvNet(
                num_inputs=input_features,
                num_channels=num_channels,
                kernel_size=kernel_size,
                dropout=dropout,
                generator=generator,
                activation=self.activation,
            ),
            nn.Conv1d(
                in_channels=num_channels[-1],
                out_channels=latent_features,
                kernel_size=1,
                padding="same",
            ),
            self.activation(),
            nn.AvgPool1d(kernel_size=pool_size, stride=None, padding=0),
        )

        self.decoder = nn.Sequential(
            nn.Upsample(scale_factor=pool_size, mode="nearest"),
            TemporalConvNet(
                num_inputs=latent_features,
                num_channels=num_channels,
                kernel_size=kernel_size,
                dropout=dropout,
                generator=generator,
                activation=self.activation,
            ),
            nn.Conv1d(
                in_channels=num_channels[-1],
                out_channels=input_features,
                kernel_size=1,
                padding="same",
            ),
        )

    def forward(self, features):
        _latent = self.encoder(features)
        _output = self.decoder(_latent)

        return _output

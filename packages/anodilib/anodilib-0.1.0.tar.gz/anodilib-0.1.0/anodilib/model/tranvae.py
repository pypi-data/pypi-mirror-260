from typing import Tuple
import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.normal import Normal
from torch.distributions.multivariate_normal import MultivariateNormal

from model.utils import PositionalEmbedding


class TranVAE(nn.Module):
    def __init__(
        self,
        input_dim: int,
        num_layers: int,
        batch_first: bool = True,
        n_z: int = 10,
        device=torch.device("cpu"),
    ):
        super(TranVAE, self).__init__()
        self.input_dim = input_dim
        self.num_layers = num_layers
        self.device = device
        self.n_z = n_z

        self.positional_embedding = PositionalEmbedding(d_model=self.input_dim)
        # Build Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.input_dim,
            dim_feedforward=self.input_dim,
            nhead=1,
            batch_first=batch_first,
        )
        encoder_norm = nn.LayerNorm(normalized_shape=self.input_dim)
        self.encoder_transformer = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=self.num_layers, norm=encoder_norm
        )

        # Latent space
        self.z_mean = nn.Linear(self.input_dim, self.input_dim)
        self.z_var = nn.Softplus()

        # Decoder, actually using same architecture as encoder
        decoder_layer = nn.TransformerEncoderLayer(
            d_model=self.input_dim,
            dim_feedforward=self.input_dim,
            nhead=1,
            batch_first=batch_first,
        )
        decoder_norm = nn.LayerNorm(normalized_shape=self.input_dim)
        self.decoder_transformer = nn.TransformerEncoder(
            encoder_layer=decoder_layer, num_layers=self.num_layers, norm=decoder_norm
        )

    def encode(self, input: torch.Tensor):
        """
        Encodes the input by passing through the encoder network
        and returns the latent codes.
        :param input: (Tensor) Input tensor to encoder [B x S x I]
        :return: (Tensor) Tuple of latent codes
        """
        e_t = self.encoder_transformer(input)
        # result = torch.flatten(result, start_dim=1)

        # Split the result into mu and var components
        # of the latent Gaussian distribution
        z_mean = self.z_mean(e_t)
        z_var = self.z_var(e_t)
        return z_mean, z_var

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """
        Maps the given latent codes
        onto the image space.
        :param z: (Tensor) [B x S x D]
        :return: (Tensor) [B x S x I]
        """
        d_t = self.decoder_transformer(z)
        return d_t

    def reparameterize(self, mu: torch.Tensor, var: torch.Tensor) -> torch.Tensor:
        """
        Reparameterization trick to sample from N(mu, var).
        :param mu: (Tensor) Mean of the latent Gaussian [B x S x D]
        :param var: (Tensor) Standard deviation of the latent Gaussian [B x S x D]
        :return: (Tensor) [B x D]
        """
        eps = torch.randn_like(var)
        return mu + eps * var

    def forward(
        self, input: torch.Tensor, **kwargs
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        positional_encoding = self.positional_embedding(input)
        input = input + positional_encoding
        mu, var = self.encode(input)
        z_drawn = torch.stack(
            [self.decode(self.reparameterize(mu=mu, var=var)) for i in range(self.n_z)],
            dim=0,
        )
        z = torch.mean(z_drawn, dim=0)

        return self.decode(z), mu, var

    def get_score(
        self,
        input: torch.Tensor,
        n_z: int = 10,
        *args,
        **kwargs,
    ):
        """
        Computes the reconstruction probability
        :param input: (Tensor) Input tensor [B x S x I]
        :return: reconstruction probability [B x S]
        """
        # need to implement as here
        # https://github.com/NetManAIOps/donut/blob/c8a44d91f102f36ba712e1e896408337501bce9b/donut/model.py#L163
        # https://tfsnippet.readthedocs.io/en/stable/api/tfsnippet.modules.html
        positional_encoding = self.positional_embedding(input)
        input = input + positional_encoding
        batch_size, seq_length, n_channels = input.shape
        z_mu, z_var = self.encode(input)
        z_drawn = torch.stack(
            [self.decode(self.reparameterize(mu=z_mu, var=z_var)) for i in range(self.n_z)],
            dim=0,
        )
        observed_mu = torch.mean(z_drawn, dim=0)
        observed_std = torch.std(z_drawn, dim=0)
        # Add a small constant to avoid zero variance
        small_constant = 1e-6
        observed_std = torch.where(observed_std < small_constant, small_constant, observed_std)

        eyes = torch.eye(n_channels).repeat(batch_size, seq_length, 1, 1).to(input.device)
        observed_cov = (eyes * observed_std.unsqueeze(2)) ** 2
        normal_dist = MultivariateNormal(observed_mu, observed_cov)
        # Fix for eval methods
        score = -1 * normal_dist.log_prob(input)
        return score


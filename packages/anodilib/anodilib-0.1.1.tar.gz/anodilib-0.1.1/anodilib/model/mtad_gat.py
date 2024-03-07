
import torch
import torch.nn as nn
from torch.distributions import Normal, kl_divergence
from torch.distributions import MultivariateNormal, Chi2
from torch.distributions.multivariate_normal import _batch_mahalanobis


class MTAD_GAT(nn.Module):
    """ MTAD-GAT model class.

    :param n_features: Number of input features
    :param window_size: Length of the input sequence
    :param out_dim: Number of features to output
    :param kernel_size: size of kernel to use in the 1-D convolution
    :param feat_gat_embed_dim: embedding dimension (output dimension of linear transformation)
           in feat-oriented GAT layer
    :param time_gat_embed_dim: embedding dimension (output dimension of linear transformation)
           in time-oriented GAT layer
    :param use_gatv2: whether to use the modified attention mechanism of GATv2 instead of standard GAT
    :param gru_n_layers: number of layers in the GRU layer
    :param gru_hid_dim: hidden dimension in the GRU layer
    :param forecast_n_layers: number of layers in the FC-based Forecasting Model
    :param forecast_hid_dim: hidden dimension in the FC-based Forecasting Model
    :param recon_n_layers: number of layers in the GRU-based Reconstruction Model
    :param recon_hid_dim: hidden dimension in the GRU-based Reconstruction Model
    :param dropout: dropout rate
    :param alpha: negative slope used in the leaky rely activation function

    """

    def __init__(
        self,
        n_features,
        window_size,
        out_dim,
        kernel_size=7,
        feat_gat_embed_dim=None,
        time_gat_embed_dim=None,
        use_gatv2=False,
        gru_n_layers=1,
        gru_hid_dim=300, #im code 150, laut paper 300
        forecast_n_layers=3,
        forecast_hid_dim=300, #im code 150, laut paper 300
        recon_n_layers=3,
        recon_hid_dim=300, #im code 150, laut paper 300
        recon_latent_dim=50,
        dropout=0.0, #not described in paper
        alpha=0.8,
        L=10 #not a magic number
    ):
        super(MTAD_GAT, self).__init__()

        self.conv = ConvLayer(n_features, kernel_size)
        self.feature_gat = FeatureAttentionLayer(n_features, window_size, dropout, alpha, feat_gat_embed_dim, use_gatv2)
        self.temporal_gat = TemporalAttentionLayer(n_features, window_size, dropout, alpha, time_gat_embed_dim, use_gatv2)
        self.gru = GRULayer(3 * n_features, gru_hid_dim, gru_n_layers, dropout)
        self.forecasting_model = Forecasting_Model(gru_hid_dim, forecast_hid_dim, out_dim, forecast_n_layers, dropout)
        self.recon_model = VAE(gru_hid_dim, recon_hid_dim, recon_latent_dim, out_dim, recon_n_layers, window_size, L=L)

    def forward(self, x):
        # x shape (b, n, k): b - batch size, n - window size, k - number of features

        self.recon_model.input = x.detach().clone()

        x = self.conv(x)
        h_feat = self.feature_gat(x)
        h_temp = self.temporal_gat(x)

        h_cat = torch.cat([x, h_feat, h_temp], dim=2)  # (b, n, 3k)

        _, h_end = self.gru(h_cat)
        h_end = h_end.view(x.shape[0], -1)   # Hidden state for last timestamp

        predictions = self.forecasting_model(h_end) #gets gru-output and predicts last value from window
        recons, loss = self.recon_model(h_end)

        return predictions, recons, loss

class ConvLayer(nn.Module):
    """1-D Convolution layer to extract high-level features of each time-series input
    :param n_features: Number of input features/nodes
    :param window_size: length of the input sequence
    :param kernel_size: size of kernel to use in the convolution operation
    """

    def __init__(self, n_features, kernel_size=7):
        super(ConvLayer, self).__init__()
        self.padding = nn.ConstantPad1d((kernel_size - 1) // 2, 0.0)
        self.conv = nn.Conv1d(in_channels=n_features, out_channels=n_features, kernel_size=kernel_size)
        self.relu = nn.ReLU()

    def forward(self, x): #according to paper just 1D-conv
        x = x.permute(0, 2, 1)
        x = self.padding(x)
        x = self.relu(self.conv(x))
        return x.permute(0, 2, 1)  # Permute back


class FeatureAttentionLayer(nn.Module):
    """Single Graph Feature/Spatial Attention Layer
    :param n_features: Number of input features/nodes
    :param window_size: length of the input sequence
    :param dropout: percentage of nodes to dropout
    :param alpha: negative slope used in the leaky rely activation function
    :param embed_dim: embedding dimension (output dimension of linear transformation)
    :param use_gatv2: whether to use the modified attention mechanism of GATv2 instead of standard GAT
    :param use_bias: whether to include a bias term in the attention layer
    """

    def __init__(self, n_features, window_size, dropout, alpha, embed_dim=None, use_gatv2=False, use_bias=True):
        super(FeatureAttentionLayer, self).__init__()
        self.n_features = n_features
        self.window_size = window_size
        self.dropout = dropout
        self.embed_dim = embed_dim if embed_dim is not None else window_size
        self.use_gatv2 = use_gatv2
        self.num_nodes = n_features
        self.use_bias = use_bias

        # Because linear transformation is done after concatenation in GATv2
        if self.use_gatv2:#standard not in use
            self.embed_dim *= 2
            lin_input_dim = 2 * window_size
            a_input_dim = self.embed_dim
        else:
            lin_input_dim = window_size
            a_input_dim = 2 * self.embed_dim

        self.lin = nn.Linear(lin_input_dim, self.embed_dim)
        self.a = nn.Parameter(torch.empty((a_input_dim, 1)))
        nn.init.xavier_uniform_(self.a.data, gain=1.414)

        if self.use_bias:
            self.bias = nn.Parameter(torch.zeros(n_features, n_features))

        self.leakyrelu = nn.LeakyReLU(alpha)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape (b, n, k): b - batch size, n - window size, k - number of features
        # For feature attention we represent a node as the values of a particular feature across all timestamps

        x = x.permute(0, 2, 1)

        # 'Dynamic' GAT attention
        # Proposed by Brody et. al., 2021 (https://arxiv.org/pdf/2105.14491.pdf)
        # Linear transformation applied after concatenation and attention layer applied after leakyrelu
        if self.use_gatv2:
            a_input = self._make_attention_input(x)                 # (b, k, k, 2*window_size)
            a_input = self.leakyrelu(self.lin(a_input))             # (b, k, k, embed_dim)
            e = torch.matmul(a_input, self.a).squeeze(3)            # (b, k, k, 1)

        # Original GAT attention
        else:
            Wx = self.lin(x)                                                  # (b, k, k, embed_dim)
            a_input = self._make_attention_input(Wx)                          # (b, k, k, 2*embed_dim)
            e = self.leakyrelu(torch.matmul(a_input, self.a)).squeeze(3)      # (b, k, k, 1)

        if self.use_bias:
            e += self.bias

        # Attention weights
        attention = torch.softmax(e, dim=2)
        attention = torch.dropout(attention, self.dropout, train=self.training)

        # Computing new node features using the attention
        h = self.sigmoid(torch.matmul(attention, x))

        return h.permute(0, 2, 1)

    def _make_attention_input(self, v):
        """Preparing the feature attention mechanism.
        Creating matrix with all possible combinations of concatenations of node.
        Each node consists of all values of that node within the window
            v1 || v1,
            ...
            v1 || vK,
            v2 || v1,
            ...
            v2 || vK,
            ...
            ...
            vK || v1,
            ...
            vK || vK,
        """

        K = self.num_nodes
        blocks_repeating = v.repeat_interleave(K, dim=1)  # Left-side of the matrix
        blocks_alternating = v.repeat(1, K, 1)  # Right-side of the matrix
        combined = torch.cat((blocks_repeating, blocks_alternating), dim=2)  # (b, K*K, 2*window_size)

        if self.use_gatv2:
            return combined.view(v.size(0), K, K, 2 * self.window_size)
        else:
            return combined.view(v.size(0), K, K, 2 * self.embed_dim)


class TemporalAttentionLayer(nn.Module):
    """Single Graph Temporal Attention Layer
    :param n_features: number of input features/nodes
    :param window_size: length of the input sequence
    :param dropout: percentage of nodes to dropout
    :param alpha: negative slope used in the leaky rely activation function
    :param embed_dim: embedding dimension (output dimension of linear transformation)
    :param use_gatv2: whether to use the modified attention mechanism of GATv2 instead of standard GAT
    :param use_bias: whether to include a bias term in the attention layer

    """

    def __init__(self, n_features, window_size, dropout, alpha, embed_dim=None, use_gatv2=True, use_bias=True):
        super(TemporalAttentionLayer, self).__init__()
        self.n_features = n_features
        self.window_size = window_size
        self.dropout = dropout
        self.use_gatv2 = use_gatv2
        self.embed_dim = embed_dim if embed_dim is not None else n_features
        self.num_nodes = window_size
        self.use_bias = use_bias

        # Because linear transformation is performed after concatenation in GATv2
        if self.use_gatv2:
            self.embed_dim *= 2
            lin_input_dim = 2 * n_features
            a_input_dim = self.embed_dim
        else:
            lin_input_dim = n_features
            a_input_dim = 2 * self.embed_dim

        self.lin = nn.Linear(lin_input_dim, self.embed_dim)
        self.a = nn.Parameter(torch.empty((a_input_dim, 1)))
        nn.init.xavier_uniform_(self.a.data, gain=1.414)

        if self.use_bias:
            self.bias = nn.Parameter(torch.zeros(window_size, window_size))

        self.leakyrelu = nn.LeakyReLU(alpha)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape (b, n, k): b - batch size, n - window size, k - number of features
        # For temporal attention a node is represented as all feature values at a specific timestamp

        # 'Dynamic' GAT attention
        # Proposed by Brody et. al., 2021 (https://arxiv.org/pdf/2105.14491.pdf)
        # Linear transformation applied after concatenation and attention layer applied after leakyrelu
        if self.use_gatv2:
            a_input = self._make_attention_input(x)              # (b, n, n, 2*n_features)
            a_input = self.leakyrelu(self.lin(a_input))          # (b, n, n, embed_dim)
            e = torch.matmul(a_input, self.a).squeeze(3)         # (b, n, n, 1)

        # Original GAT attention
        else:
            Wx = self.lin(x)                                                  # (b, n, n, embed_dim)
            a_input = self._make_attention_input(Wx)                          # (b, n, n, 2*embed_dim)
            e = self.leakyrelu(torch.matmul(a_input, self.a)).squeeze(3)      # (b, n, n, 1)

        if self.use_bias:
            e += self.bias  # (b, n, n, 1)

        # Attention weights
        attention = torch.softmax(e, dim=2)
        attention = torch.dropout(attention, self.dropout, train=self.training)

        h = self.sigmoid(torch.matmul(attention, x))    # (b, n, k)

        return h

    def _make_attention_input(self, v):
        """Preparing the temporal attention mechanism.
        Creating matrix with all possible combinations of concatenations of node values:
            (v1, v2..)_t1 || (v1, v2..)_t1
            (v1, v2..)_t1 || (v1, v2..)_t2

            ...
            ...

            (v1, v2..)_tn || (v1, v2..)_t1
            (v1, v2..)_tn || (v1, v2..)_t2

        """

        K = self.num_nodes
        blocks_repeating = v.repeat_interleave(K, dim=1)  # Left-side of the matrix
        blocks_alternating = v.repeat(1, K, 1)  # Right-side of the matrix
        combined = torch.cat((blocks_repeating, blocks_alternating), dim=2)

        if self.use_gatv2:
            return combined.view(v.size(0), K, K, 2 * self.n_features)
        else:
            return combined.view(v.size(0), K, K, 2 * self.embed_dim)


class GRULayer(nn.Module):
    """Gated Recurrent Unit (GRU) Layer
    :param in_dim: number of input features
    :param hid_dim: hidden size of the GRU
    :param n_layers: number of layers in GRU
    :param dropout: dropout rate
    """

    def __init__(self, in_dim, hid_dim, n_layers, dropout):
        super(GRULayer, self).__init__()
        self.hid_dim = hid_dim
        self.n_layers = n_layers
        self.dropout = 0.0 if n_layers == 1 else dropout
        self.gru = nn.GRU(in_dim, hid_dim, num_layers=n_layers, batch_first=True, dropout=self.dropout)

    def forward(self, x):
        out, h = self.gru(x)
        out, h = out[-1, :, :], h[-1, :, :]  # Extracting from last layer
        return out, h


class RNNDecoder(nn.Module):
    """GRU-based Decoder network that converts latent vector into output
    :param in_dim: number of input features
    :param n_layers: number of layers in RNN
    :param hid_dim: hidden size of the RNN
    :param dropout: dropout rate
    """

    def __init__(self, in_dim, hid_dim, n_layers, dropout):
        super(RNNDecoder, self).__init__()
        self.in_dim = in_dim
        self.dropout = 0.0 if n_layers == 1 else dropout
        self.rnn = nn.GRU(in_dim, hid_dim, n_layers, batch_first=True, dropout=self.dropout)

    def forward(self, x):
        decoder_out, _ = self.rnn(x)
        return decoder_out


class Forecasting_Model(nn.Module):
    """Forecasting model (fully-connected network)
    :param in_dim: number of input features
    :param hid_dim: hidden size of the FC network
    :param out_dim: number of output features
    :param n_layers: number of FC layers
    :param dropout: dropout rate
    """

    def __init__(self, in_dim, hid_dim, out_dim, n_layers, dropout):
        super(Forecasting_Model, self).__init__()
        layers = [nn.Linear(in_dim, hid_dim)]
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(hid_dim, hid_dim))

        layers.append(nn.Linear(hid_dim, out_dim))

        self.layers = nn.ModuleList(layers)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()

    def forward(self, x):
        for i in range(len(self.layers) - 1):
            x = self.relu(self.layers[i](x))
            x = self.dropout(x)
        return self.layers[-1](x)

class VAE(nn.Module):
    """
    Reconstruction-Model, fully-connected, gets reconstruction, recon prob and trainloss
    """
    def __init__(self, in_dim, hid_dim, latent_dim, out_dim, n_layers, window_size, dropout=0.0, L=4, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
        #Encoder
        enc_layers = [nn.Linear(in_dim, hid_dim), nn.ReLU()]
        for i in range(n_layers-2):
            enc_layers += [nn.Linear(hid_dim//2**i, hid_dim//2**(i+1)), nn.ReLU()]
        enc_layers += [nn.Linear(hid_dim//2**(n_layers-2), 2*latent_dim)]

        #Decoder
        dec_layers = [nn.Linear(latent_dim, hid_dim//2**(n_layers-2)), nn.ReLU()]
        for i in range(n_layers-2):
            dec_layers += [nn.Linear(hid_dim//2**(n_layers-i-2), hid_dim//2**(n_layers-i-3)), nn.ReLU()]
        dec_layers += [nn.Linear(hid_dim, out_dim*window_size*2)]

        self.encoder = nn.Sequential(*enc_layers)
        self.decoder = nn.Sequential(*dec_layers)

        self.approx_post = None
        self.prior = Normal(torch.zeros(latent_dim), torch.ones(latent_dim)) #cant be checked for cuda, so prior is in loss
        self.window_size = window_size
        self.out_dim = out_dim
        self.latent_dim = latent_dim
        self.L = L
        self.inference = False
        self.input = None #input of whole model, for inference score

    def encode(self, x):
        self.approx_post = self.encoder(x)
        return self.approx_post
    
    def decode(self, x):
        recons = self.decoder(x)
        return recons
    
    def reparameterize(self, mu: torch.Tensor, var: torch.Tensor) -> torch.Tensor:
        """
        Reparameterization trick to sample from N(mu, var).
        :param mu: (Tensor) Mean of the latent Gaussian [B x S x D]
        :param var: (Tensor) Standard deviation of the latent Gaussian [B x S x D]
        :return: (Tensor) [B x D]
        """
        eps = torch.randn_like(var)
        return mu + eps * var

    def forward(self, x):

        params = self.encode(x) # bs x gru_hidn ->bs x latent_dim * 2
        d = params.shape[1]
        mu = params[:, :d // 2]
        sigma_params = params[:, d // 2:]
        sigma = nn.Softplus()(sigma_params)
        self.approx_post = Normal(mu, sigma)
        
        #L-mal samplen
        out = []
        for i in range(self.L):
            self.z = self.reparameterize(mu=mu, var=sigma).to(device=x.device)
            out.append(self.decode(self.z))#bs x latent_dim -> bs x out_dim = 96*6 (zeitreihe)
        recons = torch.stack(out, dim=1)


        out_d = recons.shape[2]
        out_mu = recons[:, :, :out_d // 2]
        out_sigma_params = recons[:, :, out_d // 2:]
        out_sigma = nn.Softplus()(out_sigma_params)

        # B x L x (window*outdim) -> B x L x window x outdim
        out_mu = out_mu.view(x.shape[0], self.L, self.window_size, self.out_dim)
        out_sigma = out_sigma.view(x.shape[0], self.L, self.window_size, self.out_dim)

        # From Jelle and Daniel 25.08.
        #gets cdf of multivariate of distribution
        def multivariate_normal_dist_cdf(dist, x):
            diff = x - dist.loc
            n = dist._unbroadcasted_scale_tril.to(device=diff.device)
            M = _batch_mahalanobis(n, diff).cpu()
            
            chi2_dist = Chi2(x.shape[0]) #can't get this on GPU because of inner torch-implementation

            return 1 - chi2_dist.cdf(M)

        if self.inference: #reconstruction probability
            out_mu = out_mu.permute(0,1,3,2) #B x L x window x outdim -> B x L x outdim x window
            out_sigma = out_sigma.permute(0,1,3,2)

            probs = torch.zeros(x.shape[0], self.out_dim).to(x.device)
            for i in range(self.L):

                eyes = torch.eye(self.window_size).repeat(x.shape[0], self.out_dim, 1,1)
                out_cov = out_sigma[:,i].to(device=eyes.device)
                observed_cov = (eyes * out_cov.unsqueeze(2)) ** 2
                multivariate_normal_dist = MultivariateNormal(out_mu[:,i], observed_cov)

                new_x = self.input[:].permute(0,2,1)
                new_x.to(device = x.device)

                score = multivariate_normal_dist_cdf(multivariate_normal_dist, new_x)       
                probs += score.to(x.device)

            probs /= self.L
            
            return recons, probs
        else: #expected NLL mit Monte Carlo sampling
            probs = torch.zeros_like(self.input).to(x.device)
            for i in range(self.L):
                out_normal = Normal(out_mu[:, i], out_sigma[:, i])
                #cdf is bad, if x-values (far) outside of std, cause cdf then always makes 0 or 1
                probs += out_normal.log_prob(self.input)
            probs /= self.L
            
            prior = Normal(torch.zeros(self.latent_dim, device=x.device), torch.empty(self.latent_dim, device=x.device).fill_(sigma.max())) #torch.ones(self.latent_dim, device=x.device))
            enll = - probs.mean(dim=(1,2))
            kl_div = kl_divergence(self.approx_post, prior).sum(dim=(1))
            
            return recons, (enll, kl_div) #loss = enll + kl_div

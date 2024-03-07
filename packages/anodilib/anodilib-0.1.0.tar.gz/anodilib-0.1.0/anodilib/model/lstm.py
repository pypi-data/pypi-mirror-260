import torch
import torch.nn as nn


class ImprovedLSTMCell(torch.nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size

        # forget gate bias initialization value
        self.forget_bias_init = 1

        # create LSTM parameters
        self.W_if = torch.nn.Parameter(torch.Tensor(input_size, hidden_size))
        self.W_hf = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.W_cf = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.b_f = torch.nn.Parameter(torch.Tensor(hidden_size))

        self.W_i_c_strich = torch.nn.Parameter(torch.Tensor(input_size, hidden_size))
        self.W_h_c_strich = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.b_c_strich = torch.nn.Parameter(torch.Tensor(hidden_size))

        self.W_io = torch.nn.Parameter(torch.Tensor(input_size, hidden_size))
        self.W_ho = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.b_o = torch.nn.Parameter(torch.Tensor(hidden_size))

        self.W_ip = torch.nn.Parameter(torch.Tensor(input_size, hidden_size))
        self.W_hp = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.b_p = torch.nn.Parameter(torch.Tensor(hidden_size))

        self.W_hh = torch.nn.Parameter(torch.Tensor(hidden_size, hidden_size))
        self.b_h = torch.nn.Parameter(torch.Tensor(hidden_size))

        # initialize parameters
        self.reset_parameters()

    def forward(self, input, hx):
        x_t = input

        h_t_layer, c_t_layer = hx

        # forget gate
        f_t = torch.sigmoid(
            x_t @ self.W_if + h_t_layer @ self.W_hf + c_t_layer @ self.W_cf + self.b_f
        )

        # cell gate
        c_strich_t = torch.tanh(
            x_t @ self.W_i_c_strich + h_t_layer @ self.W_h_c_strich + self.b_c_strich
        )

        # update cell state
        c_tp1_layer = f_t * c_t_layer + c_strich_t * (1 - f_t)

        # output gate
        o_t = torch.sigmoid(x_t @ self.W_io + h_t_layer @ self.W_ho + self.b_o)

        # P_t
        p_t = torch.tanh(x_t @ self.W_ip + h_t_layer @ self.W_hp + self.b_p)

        # update hidden state
        h_tp1_layer = o_t * torch.tanh(c_tp1_layer) + (1 - o_t) * p_t

        return h_tp1_layer, c_tp1_layer

    def reset_parameters(self):
        std = 1.0 / (self.hidden_size**0.5)
        for weight in self.parameters():
            weight.data.uniform_(-std, std)

        # set forget gate bias to initialization value
        self.b_f.data.fill_(self.forget_bias_init)


class ImprovedLSTM(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1, dropout=0, device=torch.device("cpu")):
        super().__init__()
        self.device = device

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout

        # forget gate bias initialization value
        self.forget_bias_init = 1

        self.lstm_cells = []
        for layer in range(num_layers):
            layer_input_size = input_size if layer == 0 else hidden_size
            self.lstm_cells.append(ImprovedLSTMCell(layer_input_size, hidden_size))

        self.lstm_cells = nn.ModuleList(self.lstm_cells)
        self.output_size = hidden_size

        self.fc = nn.Linear(self.output_size, self.input_size)

    def forward(self, input, hx=None):
        if hx is None:
            hx = [
                (
                    torch.zeros(input.size(1), self.hidden_size, device=self.device),
                    torch.zeros(input.size(1), self.hidden_size, device=self.device),
                )
                for _ in range(self.num_layers)
            ]

        # apply dropout to input
        if self.dropout > 0:
            input = torch.nn.functional.dropout(
                input, p=self.dropout, training=self.training
            )

        layer_output = input
        last_states = []
        for layer in range(self.num_layers):
            cell_output = []
            hx_layer = hx[layer]
            for seq in range(layer_output.size(0)):
                hx_layer = self.lstm_cells[layer](layer_output[seq], hx_layer)
                cell_output.append(hx_layer[0])
            layer_output = torch.stack(cell_output)
            last_states.append(hx_layer)

        logits = self.fc(layer_output)
        return logits, last_states

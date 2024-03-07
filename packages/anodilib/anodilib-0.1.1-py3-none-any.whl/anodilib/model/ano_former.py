import torch
import torch.nn as nn
from model.utils import *
import torch.nn.functional as F
import numpy as np
import math

class AnoFormer(nn.Module):
    def __init__(self,
                 n_critic, #number of critic train iterations befor next generator iteration
                 input_length,d,L,K,dim_num,substitute_value,dim_feedforward,
                 Llambda, #gradient penalty lambda
                 critic_opt, #optimizer for the critic training phase
                 critic_lr,
                 critic_L,
                 p=0.25,
                 beta = 1e10, #soft-argmax to function properly
                 verbose = False,
                 *args, **kwargs) -> None:
        """
        AnoFormer from "Time Series Anomaly Detection Using Transformer-Based GAN With Two-Step Masking"
        by AH-HYUNG SHIN , SEONG TAE KIM , (Member, IEEE), AND GYEONG-MOON PARK
        """
        super().__init__(*args, **kwargs)

        self.n_critic = n_critic
        self.Llambda = Llambda
        self.critic_lr = critic_lr
        self.critic_L = critic_L
        self.verbose = verbose

        self.generator = Generator(input_length,d,L,K,p,dim_num,beta,substitute_value, dim_feedforward=dim_feedforward) #guessed, but embeding dim has to be divideable by nhaeds
        self.critic = Critic(input_length=input_length, K=K, d=d, L=self.critic_L, dim_num=dim_num, dim_feedforward=dim_feedforward)

        
        self.critic_opt = critic_opt(self.critic.parameters(), lr=self.critic_lr)

        self.train_phase = True
        self.critic_train_count = 0

    def forward(self, x):
        """if self.train_phase returns loss, e.g. critic-/generator-loss
           else returns reconstruction error of generator output"""
        # partly from https://github.com/igul222/improved_wgan_training/tree/master
        if self.train_phase:
            
            critic_losses = 0
            # whole critic functionality isnt really tested. Its from the paper, but was found unnecessary during development
            # so generator only archtitecture, use critic code with caution, its untested in this state and has development commented code
            while self.critic_train_count < self.n_critic:
                #critic training phase
                self.critic_opt.zero_grad()
                
                if self.critic_train_count == self.n_critic-1:
                    self.generator_out = self.generator(x)
                else:
                    with torch.no_grad():
                        self.generator_out = self.generator(x) #without opt step

                self.critic_train_count += 1

                self.fake_data = self.critic(self.generator_out)
                self.real_data = self.critic(x)

                # real + a * fake - a*real #from github
                # is it the same?
                # fake - a * fake + a*real
                # = a*real + (1-a)*fake #from paper
                epsilon = torch.rand(1).to(x.device)
                x_strich = epsilon * x + (1-epsilon) * self.generator_out

                x_strich_out = self.critic(x_strich, loss_calc=True)
                # from https://discuss.pytorch.org/t/newbie-pytorch-equivalent-of-tf-tf-gradients-out-in/130988
                # should be grad from x_strich, but embedding messes with gradients so its from the embedding weights
                # gradients = torch.autograd.grad(x_strich_out, self.critic.embedding.token.weight, torch.ones_like(x_strich_out), retain_graph=True)[0]
                critic_loss = self.L_c_adv(x_hat=self.fake_data, x_snake=self.real_data)#, gradients=gradients)

                # return self.generator_out, self.fake_data, critic_loss

                critic_loss.backward(retain_graph=True)
                self.critic_opt.step()
                critic_losses += critic_loss
            
            if self.verbose:
                print(f"Mean critic loss of the {self.n_critic} critic-batches: {(critic_losses/self.n_critic).mean().item():.4f}")
            self.critic_train_count = 0
            #generator training phase
            #generator_loss = self.lambda_rec * self.L_g_rec(self.generator_out, x) + self.lambda_adv * self.L_g_adv(self.fake_data)

            self.generator_out = self.generator(x)
            self.fake_data = torch.Tensor([0]).to(x.device)

            return self.generator_out, self.fake_data
            
        else:
            #predict
            self.critic_train_count = 0

            # not really described, just take mse as anomaly score 
            self.generator_out = self.generator(x)

            return self.generator_out #F.mse_loss(self.generator_out, x)
    
    def L_c_adv(self, x_hat, x_snake, gradients=0): #currently weighted with 0
        # real_label = torch.ones_like(x_hat).to(x_hat.device)
        # real_label[:,0] = 0.0
        # fake_label = torch.zeros_like(x_hat).to(x_hat.device)
        # fake_label[:, 0] = 1.0
        # classif_of_real = F.cross_entropy(x_hat, real_label)
        # classif_of_fake = F.cross_entropy(x_snake, fake_label)
        # # return classif_of_real + classif_of_fake

        disc_cost = x_hat.mean() - x_snake.mean()
        # slopes = torch.sqrt(torch.sum(torch.square(gradients), dim=1)) #if critic-output is shape bs x 1, sum(dim=1) is a bit pointless ?!
        # gradient_penalty = torch.sum((slopes-1.0)**2)
        return disc_cost #+ self.Llambda * gradient_penalty
    
    def L_g_rec(self, x_hat, x_snake):
        return F.mse_loss(x_hat, x_snake) #should be F.cross_entropy(x_hat, x_snake), but doesnt work

    def L_g_adv(self,x_hat): #currently weighted with 0
        return - torch.mean(x_hat)

class Generator(nn.Module):
    def __init__(self, 
                 input_length,
                 d,
                 L, #number of Transformer-Layers
                 K,
                 p, #percent of remasking
                 dim_num,
                 beta: int = 12, #paper said 1000, but e^1000 -> inf, so we take just 12
                 substitute_value = lambda x: 0, #masked values, could be mean, 1, or ..., lambda gets input batch
                 nheads = 8, #is probably overridden by d
                 dim_feedforward = 1024,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.input_length = input_length
        self.d = d
        self.L = L
        self.K = K
        self.p = p
        self.dim_num = dim_num
        self.beta = beta
        self.substitute_value = substitute_value

        # paper says K+1 vectors for mask-Token extra, but we save the token externally
        self.embedding = BERTEmbedding(vocab_size=self.K, embed_size=self.d)
        
        nheads = dim_num #in MultiHeadAttention embed_dim(=self.d*dim_num) must be divisible by num_heads, so just set nheads to TokenEmbedding dim
        self.transformer_layer = nn.TransformerEncoderLayer(self.d*dim_num,
                                                            nhead=nheads,
                                                            dim_feedforward=dim_feedforward,
                                                            batch_first=True) #parameter suchen
        self.transformer = nn.TransformerEncoder(self.transformer_layer, self.L)

    def forward(self, x):
        
        #Step 1 Masking

        #masking, make substitute value where masking1 == True
        masking1 = self.get_mask(x, mask_pct=0.1, mask_stride_pct=0.5)
        masked = x
        masked[masking1] = torch.tensor(self.substitute_value(x), device=x.device).float().expand(*x.shape)[masking1]

        embedding_out = self.embedding(masked)

        #make bs x seq len x feature count x embedding dim to bs x seq len x feature count*embedding dim for transformer
        embedding_out = nn.Flatten(start_dim=2)(embedding_out)

        #compute transformer output + attention-maps for re-masking
        #from https://discuss.pytorch.org/t/extracting-self-attention-maps-from-nn-transformerencoder/139998
        attention_maps = []
        norm_first = self.transformer.layers[0].norm_first

        # brauchen wir die?
        mask = None
        src_key_padding_mask = None
        for i in range(self.L):
            # compute attention of layer i
            h = embedding_out.clone()
            if norm_first:
                h = self.transformer.layers[i].norm1(h)
            attn_logits,attn_probs  = self.transformer.layers[i].self_attn(h, h, h,attn_mask=mask,key_padding_mask=src_key_padding_mask,need_weights=True)
            attention_maps.append(attn_probs) #maybe should be attn_logits reshaped to bs x seq len x feature count x embedding dim
            # forward of layer i
            embedding_out = self.transformer.layers[i](embedding_out,src_mask=mask,src_key_padding_mask=src_key_padding_mask)
        
        assert self.dim_num == x.shape[2], "x should be bs x seq len x feature count"
        embedding_out = torch.unflatten(embedding_out, dim=2, sizes=(x.shape[2], self.d)) #bs x seq len x feature count x embedding dim

        # embedding_out really should be transformer_out1 after first iteration
        cos = []
        for i in range(embedding_out.shape[2]): #for every feature one normalization
            #cosine norm by hand cause torch makes it weird
            cos.append((embedding_out[:,:,i] @ self.embedding.token.weight.T[None,:,:]) / \
                                    (torch.norm(embedding_out[:,:,i], dim=(1,2)) * torch.norm(self.embedding.token.weight.T, dim=(0,1)) + \
                                      1e-10)[:, None, None]) #add dimensions for torch broadcasting

        cos = torch.stack(cos, dim=1) #stack as bs x features x seq len x K
        p_hat = F.softmax(cos, dim=2) #cause here we need to softmax without features

        #soft-argmax to get back quantized ints as timeseries
        # inds = torch.arange(0, self.K).expand(*p_hat.shape).to(x.device)
        # output_X1_hat = torch.sum(torch.exp(self.beta * p_hat) / torch.sum(torch.exp(self.beta * p_hat), dim=3)[:,:,:,None] * inds, dim=3)

        # from https://github.com/david-wb/softargmax/tree/master
        *_, n = p_hat.shape
        p_hat = nn.functional.softmax(self.beta * p_hat, dim=-1)
        indices = torch.linspace(0, 1, n, requires_grad=True, device=x.device)
        output_X1_hat = torch.sum((n - 1) * p_hat * indices, dim=-1)
        output_X1_hat = output_X1_hat.permute(0,2,1) #reshape from bs x features x seq len to bs x seq len x features
        # soft-argmax produces values close to K/2, in K<50 the relative deviation is big, but with K>>100 its in <1% range of K

        #Step 2 Masking

        # get entropy from attention maps for remasking
        attention_maps = torch.stack(attention_maps, dim=0)
        # self.transformer.layers[i].self_attn() already has softmax
        entropy = torch.sum(torch.sum(attention_maps*torch.log(attention_maps), dim=2), dim=0) * (-1.0/self.L) #dont know which of seq len dim to sum over, 2/3
        
        # get indices of self.p% highest entropy from the parts, that were masked in step 1, e.g. were put to substitute value
        # "~" makes boolean inverse
        # first masking is over features aswell, but in attention maps features are ignored so second masking can only be over bs, sequence
        masking1 = masking1.sum(dim=2).to(dtype=torch.bool)
        entropy[~masking1] = -10 #-float("inf") #if this doesnt work just make "-10"
        remask_idzs = torch.argsort(entropy, dim=0)[:, -int(entropy.shape[1]*self.p):] 

        # combine new mask and masking1 so that all unmasked from step 1 + the self.p% highest entropy values are masked in step 2 
        masking2 = ~masking1
        masking2[remask_idzs] = True

        masked2 = x
        masked2[masking2] = torch.tensor(self.substitute_value(x), device=x.device).float().expand(*x.shape)[masking2]
        

        embedding_out2 = self.embedding(masked2)
        embedding_out2 = nn.Flatten(start_dim=2)(embedding_out2)
        transformer_out2 = self.transformer(embedding_out2)
        transformer_out2 = torch.unflatten(transformer_out2, dim=2, sizes=(x.shape[2], self.d)) #bs x seq len x feature count x embedding dim
        
        cos2 = []
        for i in range(transformer_out2.shape[2]): #for every feature one normalization
            #cosine norm by hand cause torch makes it weird
            cos2.append((transformer_out2[:,:,i] @ self.embedding.token.weight.T[None,:,:]) / \
                                    (torch.norm(transformer_out2[:,:,i], dim=(1,2)) * torch.norm(self.embedding.token.weight.T, dim=(0,1)) + \
                                      1e-10)[:, None, None]) #add dimensions for torch broadcasting

        cos2 = torch.stack(cos2, dim=1) #stack as bs x features x seq len x K
        p_hat2 = F.softmax(cos2, dim=2) #cause here we need to softmax without features

        #soft-argmax to get back quantized ints as timeseries
        # inds2 = torch.arange(0, self.K).expand(*p_hat2.shape).to(x.device)
        # output_X2_hat = torch.sum(torch.exp(self.beta * p_hat2) / torch.sum(torch.exp(self.beta * p_hat2), dim=3)[:,:,:,None] * inds2, dim=3)
        # output_X2_hat = output_X2_hat.reshape(*x.shape) #reshape from bs x features x seq len to bs x seq len x features

        # from https://github.com/david-wb/softargmax/tree/master
        *_, n = p_hat2.shape
        p_hat2 = nn.functional.softmax(self.beta * p_hat2, dim=-1)
        indices = torch.linspace(0, 1, n, requires_grad=True, device=x.device)
        output_X2_hat = torch.sum((n - 1) * p_hat2 * indices, dim=-1)
        output_X2_hat = output_X2_hat.permute(0,2,1)

        # the lowest (1-self.p%) entropy-elements should be kept from step 1 for output, the rest is taken from step 2 
        # output = output_X1_hat[~masking2] + output_X2_hat[masking2]
        output = torch.where(masking2[:,:,None], output_X2_hat, output_X1_hat)# if masking2 True X2 else X1

        return output

    @staticmethod
    def get_mask(X, mask_pct=0.1, mask_stride_pct=0.5):
        batch_size, seq_length, n_channels = X.shape

        mask_length = math.ceil(mask_pct * seq_length)
        mask_stride = math.floor(mask_stride_pct * mask_length)
        if mask_stride == 0: mask_stride = 1
        mask_num = math.floor(2 * mask_length / mask_stride) #if zero devision error, the window length is too short for a reasonable masking
        mask = torch.zeros_like(X)
        
        # ToDo: vectorize this
        possible_starting_positions = np.arange(math.ceil((seq_length - mask_length) / mask_stride)) * mask_stride
        starting_positions = np.zeros((batch_size, n_channels, mask_num), dtype=np.int32)
        # Generate unique starting positions for each sequence without replacement
        for i in range(batch_size):
            for j in range(n_channels):
                starting_positions = np.random.choice(possible_starting_positions, mask_num, replace=False)
                seq_mask = (torch.arange(mask_length)[:, None] + starting_positions).reshape(-1)
                mask[i, seq_mask, j] = 1.0
        
        mask = mask.type(torch.bool)
        return mask
    
class Critic(nn.Module):
    def __init__(self,
                 input_length,
                 K,
                 d,
                 L = 6, #transformer count
                 dim_num = 5,
                 nheads = 8, #is probably overridden by d
                 dim_feedforward = 1024,
                 *args, **kwargs) -> None:
        """critic from GAN-architecture, but untested in currently not in development, use generator only"""
        super().__init__(*args, **kwargs)

        self.input_length = input_length
        self.K = K
        self.d = d
        self.L = L
        self.dim_num = dim_num

        self.embedding = BERTEmbedding(vocab_size=self.K, embed_size=self.d)
        
        nheads = self.d #in MultiHeadAttention embed_dim(=self.d*dim_num) must be divisible by num_heads, so just set nheads to TokenEmbedding dim
        if L > 0:
            self.transformer_layer = nn.TransformerEncoderLayer(self.d*dim_num,
                                                                nhead=nheads,
                                                                dim_feedforward=dim_feedforward,
                                                                batch_first=True) #parameter suchen
            self.transformer = nn.TransformerEncoder(self.transformer_layer, self.L)
            transformer_out_size = self.input_length * self.dim_num * self.d #could potentially get very big

            self.classifier = nn.Linear(transformer_out_size, 2)
        
    def forward(self, x, loss_calc=False):
        if self.L <= 0:
            print("no transformer stack and linear layer initialized, no forward possible. L = ", self.L)
        if loss_calc:
            ohmat = F.one_hot(x.long(), num_classes=self.K).float()
            # bi = torch.tensor([[[0,1,0], [1,0,0]]], dtype=torch.float32) example
            # bi.requires_grad = True #hopefully not needed
            embedding_out = torch.matmul(ohmat, self.embedding.token.weight)
        else:
            embedding_out = self.embedding(x)
        embedding_out = nn.Flatten(start_dim=2)(embedding_out)
        transformer_out = self.transformer(embedding_out)
        transformer_out = torch.unflatten(transformer_out, dim=2, sizes=(x.shape[2], self.d)) #bs x seq len x feature count x embedding dim
        out = self.classifier(nn.Flatten(start_dim=1)(transformer_out)) #maybe put an activation over it to map between 0 and 1 or so?!
        out = F.softmax(out, dim=1)
        return out

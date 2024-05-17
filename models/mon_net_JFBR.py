import torch
from models.base_mon_net import MonLayer, BaseMonNet

# training approach inspired by CSBO paper https://arxiv.org/abs/2310.18535
class MonNetJFBR(BaseMonNet):
    """ Monotone network trained using standard automatic differentiation (AD). """

    def __init__(self, in_dim, out_dim, m=1.0, max_iter=100, tol=1e-6):
        super().__init__(in_dim, out_dim, m, max_iter, tol)
    
    def name(self):
        return 'MonNetJFBR'

    def forward(self, x, z=None):
        z = torch.zeros(self.out_dim) if z is None else z
        
        # Training
        if self.training:
            # generate probablity vector p[k] using truncated geometric distribution then sample k
            p = torch.zeros(self.max_iter)
            for k in range(self.max_iter):
                p[k] = 2**(self.max_iter - k) / (2**(self.max_iter + 1) - 1)
            assert torch.isclose(torch.sum(p), torch.tensor(1.0)), 'p is not a probability vector'

            sampled_k = torch.multinomial(p, 1).item()
            
            # Compute z_1 
            z = self.mon_layer(x, z)
            z_1 = z

            # Compute z_k
            with torch.no_grad():
                for _ in range(sampled_k - 2):
                    z = self.mon_layer(x, z)
            z = self.mon_layer(x, z)
            z_k = z

            # Compute z_{k+1}
            z.detach()
            z = self.mon_layer(x, z)
            z_k_1 = z

            return z_1, z_k, z_k_1

        # Evaluation
        else:
            for _ in range(self.max_iter):
                z_new = self.mon_layer(x, z)
                if torch.norm(z_new - z, p=2) < self.tol:
                    z = z_new
                    break
                z = z_new
            return z
    
    def train_step(self, X_batch, Y_batch, ):
        self.optimizer.zero_grad()
        Y_hat = self.forward(X_batch)
        loss = self.criterion(Y_hat, Y_batch)
        loss.backward()
        self.optimizer.step()
        return loss.item()
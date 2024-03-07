import numpy as np
from math import exp

np.random.seed(0)
class VanillaRecurrentNetwork(object):

    def __init__(self):
        self.hidden_state = np.zeros((3, 3))
        self.W_hh = np.random.randn(3, 3)
        self.W_xh = np.random.randn(3, 3)
        self.W_hy = np.random.randn(3, 3)
        self.Bh = np.random.randn(3,)
        self.By = np.random.rand(3,)

        self.hidden_state_activation_function = lambda x : np.tanh(x)
        self.y_activation_function = lambda x : x

        self.loss_funciton = lambda y : exp(y) / np.sum(exp(y))

    def forward_prop(self, x):
        self.hidden_state = self.hidden_state_activation_function(
            np.dot(self.hidden_state, self.W_hh) + np.dot(x, self.W_xh) + self.Bh
        )

        return self.y_activation_function(self.W_hy.dot(self.hidden_state) + self.By)

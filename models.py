import torch
import torch.nn as nn
import numpy as np

class FCsmall(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(FCsmall, self).__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(nn.Linear(input_dim, 50),
                                 nn.ReLU(),
                                 nn.Linear(50, output_dim))

    def forward(self, x):
        if len(x.shape) >= 3:
            x = x.reshape(x.shape[0], x.shape[1] * x.shape[2])
        else:
            x = x.reshape(x.numel(), )
        x = self.net(x)
        return x


class FCsmallSM(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(FCsmallSM, self).__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(nn.Linear(input_dim, 50),
                                 nn.ReLU(),
                                 nn.Linear(50, output_dim))
        self.sm = nn.Softmax()

    def forward(self, x):
        if len(x.shape) >= 3:
            x = x.reshape(x.shape[0], x.shape[1] * x.shape[2])
        else:
            x = x.reshape(x.numel(), )
        x = self.net(x)
        x = self.sm(x)
        return x


class FCmedium(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(FCmedium, self).__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(nn.Linear(input_dim, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 64),
                                 nn.ReLU(),
                                 nn.Linear(64, 32),
                                 nn.ReLU(),
                                 nn.Linear(32, 16),
                                 nn.ReLU(),
                                 nn.Linear(16, output_dim))

    def forward(self, x):
        if len(x.shape) >= 3:
            x = x.reshape(x.shape[0], x.shape[1] * x.shape[2])
        else:
            x = x.reshape(x.numel(), )
        x = self.net(x)
        return x


class FCmediumSM(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(FCmediumSM, self).__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(nn.Linear(input_dim, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 64),
                                 nn.ReLU(),
                                 nn.Linear(64, 32),
                                 nn.ReLU(),
                                 nn.Linear(32, 16),
                                 nn.ReLU(),
                                 nn.Linear(16, output_dim))
        self.sm = nn.Softmax()

    def forward(self, x):
        if len(x.shape) >= 3:
            x = x.reshape(x.shape[0], x.shape[1] * x.shape[2])
        else:
            x = x.reshape(x.numel(), )
        x = self.net(x)
        x = self.sm(x)
        return x


class CNNsmall(nn.Module):
    def __init__(self, in_ch, output_dim):
        super(CNNsmall, self).__init__()
        self.net = nn.Sequential(nn.Conv2d(in_ch, 8, 3),
                                 nn.ReLU(),
                                 nn.Conv2d(8, 1, 3),
                                 nn.ReLU())
        self.out = nn.Linear(6*1, output_dim)
        
    def forward(self, x):
        if len(x.shape) >= 3:
            x = x[:, None, :, :]
        else:
            x = x[None, :, :]
        x = self.net(x)
        if len(x.shape) >= 4:
            x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
        else:
            x = x.reshape(x.numel(), )
        x = self.out(x)
        return x


class CNNsmallSM(nn.Module):
    def __init__(self, in_ch, output_dim):
        super(CNNsmallSM, self).__init__()
        self.net = nn.Sequential(nn.Conv2d(in_ch, 8, 3),
                                 nn.ReLU(),
                                 nn.Conv2d(8, 1, 3),
                                 nn.ReLU(),
                                 nn.Linear(6*1, output_dim))
        self.sm = nn.Softmax()
        
    def forward(self, x):
        x = self.net(x)
        x = self.sm(x)
        return x


class CNNmedium(nn.Module):
    def __init__(self, in_ch, output_dim):
        super(CNNmedium, self).__init__()
        self.net = nn.Sequential(nn.Conv2d(in_ch, 64, 3),
                                 nn.ReLU(),
                                 nn.Conv2d(64, 16, 3, padding=1),
                                 nn.ReLU(), 
                                 nn.Conv2d(16, 1, 3), 
                                 nn.ReLU())
        self.out = nn.Linear(6*1, output_dim)
        
    def forward(self, x):
        if len(x.shape) >= 3:
            x = x[:, None, :, :]
        else:
            x = x[None, :, :]
        x = self.net(x)
        if len(x.shape) >= 4:
            x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3])
        else:
            x = x.reshape(x.numel(), )
        x = self.out(x)
        return x

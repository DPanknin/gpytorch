#!/usr/bin/env python3

import torch

from .mean import Mean


class ConstantMeanGrad(Mean): # TODO added by DANNY (only derivative case)
    def __init__(self, prior=None, batch_shape=torch.Size(), onlyDerivative=False, **kwargs):
        super(ConstantMeanGrad, self).__init__()
        self.batch_shape = batch_shape
        if onlyDerivative:
            self.constant = torch.zeros(*batch_shape, 1)
        else:
            self.register_parameter(name="constant", parameter=torch.nn.Parameter(torch.zeros(*batch_shape, 1)))
            if prior is not None:
                self.register_prior("mean_prior", prior, "constant")
        self.onlyDerivative = onlyDerivative

    def forward(self, input):
        batch_shape = torch.broadcast_shapes(self.batch_shape, input.shape[:-2])
        if self.onlyDerivative:
            mean = self.constant.unsqueeze(-1).expand(*batch_shape, input.size(-2), input.size(-1)).contiguous()
            mean[..., :] = 0
        else:
            mean = self.constant.unsqueeze(-1).expand(*batch_shape, input.size(-2), input.size(-1) + 1).contiguous()
            mean[..., 1:] = 0
        return mean

import numpy as np
import torch

import sukta.tree_util as stu


def clone(x):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: lambda v: v.clone(),
                np.ndarray: lambda v: v.copy(),
            },
            fallback=lambda v: v,
        ),
        x,
    )


def detach(x):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: lambda v: v.detach(),
            },
            fallback=lambda v: v,
        ),
        x,
    )


def to_batch(x):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor | np.ndarray: lambda v: v[None, ...],
                type(None): lambda v: v,
            },
            fallback=lambda v: v,
        ),
        x,
    )


def to_device(x, device):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: lambda v, d=device: v.to(d),
                type(None): lambda v: v,
            },
        ),
        x,
    )


def to_tensor(x):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: lambda v: v,
                np.ndarray: torch.from_numpy,
                type(None): lambda v: v,
            }
        ),
        x,
    )


def to_numpy(x):
    def f(tensor):
        if tensor.is_cuda:
            return tensor.detach().cpu().numpy()
        else:
            return tensor.detach().numpy()

    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: f,
                np.ndarray: lambda x: x,
                type(None): lambda x: x,
            },
        ),
        x,
        dict_type=dict | torch.nn.ParameterDict,
    )

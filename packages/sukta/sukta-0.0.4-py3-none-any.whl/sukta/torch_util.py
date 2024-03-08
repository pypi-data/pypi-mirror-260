import typing as tp

import sukta.tree_util as stu


def num_params(model: "torch.nn.Module", requires_grad: bool = True):
    return sum(
        p.numel() for p in model.parameters() if (not requires_grad) or p.requires_grad
    )


def to_device(tree: tp.Dict, device: str):
    _to_device: tp.Callable[["torch.Tensor"], "torch.Tensor"] = lambda x: x.to(device)
    return stu.apply_vfunc(_to_device, tree)

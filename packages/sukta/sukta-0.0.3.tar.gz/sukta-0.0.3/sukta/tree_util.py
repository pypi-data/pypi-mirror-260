import typing as tp


def iter_path(d: tp.Dict, prefix: tp.Tuple = (), delim: str = "/"):
    """
    generator that outputs (key_path, value)
    key_path is prefix + subsequent keys of a PyTree to seperated by delim

    Args:
    """
    if isinstance(d, dict):
        for k, v in d.items():
            yield from iter_path(v, prefix + (k,))
    else:
        yield "/".join(prefix), d


def apply_vfunc(vfunc, data):
    """
    Args:
        vfunc: value function i.e. lambda v: v
    """
    if isinstance(data, dict):
        return {k: apply_vfunc(vfunc, v) for k, v in data.items()}
    return vfunc(data)

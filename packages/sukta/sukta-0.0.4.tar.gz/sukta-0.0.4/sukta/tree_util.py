from typing import Any, Callable, Dict, List, Type


def iter_path(
    d: Dict,
    prefix: List = [],
    delim: str | None = None,
    dict_type: Type = dict,
    list_type: Type = list | tuple,
    match_key: str | None = None,
):
    """
    generator that outputs (key_path, value)
    key_path is prefix + subsequent keys of a PyTree to separated by delim if specified else a list
    """
    if isinstance(d, dict_type):
        for k, v in d.items():
            if k == match_key:
                if delim is None:
                    yield prefix, v
                else:
                    yield delim.join(prefix), v
            else:
                yield from iter_path(
                    v, prefix + [k], delim, dict_type, list_type, match_key
                )
    elif isinstance(d, list_type):
        for i, v in enumerate(d):
            yield from iter_path(
                v, prefix + [str(i)], delim, dict_type, list_type, match_key
            )
    else:
        if match_key is None:
            if delim is None:
                yield prefix, d
            else:
                yield delim.join(prefix), d


def apply_vfunc(
    vfunc,
    data,
    dict_type: Type = dict,
    list_type: Type = list | tuple,
    preserve_ret_type: bool = False,
):
    """
    Args:
        vfunc: value function i.e. lambda v: v
    Returns:
        data with vfunc applied to each leaf
    """
    if isinstance(data, dict_type):
        ret_type = type(data) if preserve_ret_type else dict
        return ret_type(
            {k: apply_vfunc(vfunc, v, dict_type, list_type) for k, v in data.items()}
        )
    elif isinstance(data, list_type):
        ret_type = type(data) if preserve_ret_type else list
        return ret_type([apply_vfunc(vfunc, v, dict_type, list_type) for v in data])
    return vfunc(data)


def apply_pfunc(
    pfunc,
    data,
    prefix: List = [],
    delim: str | None = None,
    dict_type: Type = dict,
    list_type: Type = list | tuple,
    preserve_ret_type: bool = False,
):
    """
    Args:
        pfunc: <path, value> function i.e. lambda p, v: v
    Return:
        data with pfunc applied to each leaf
    """
    if isinstance(data, dict_type):
        ret_type = type(data) if preserve_ret_type else dict
        return ret_type(
            {
                k: apply_pfunc(pfunc, v, prefix + [k], delim, dict_type, list_type)
                for k, v in data.items()
            }
        )
    elif isinstance(data, list_type):
        ret_type = type(data) if preserve_ret_type else dict
        return ret_type(
            [
                apply_pfunc(pfunc, v, prefix + [str(i)], delim, dict_type, list_type)
                for i, v in enumerate(data)
            ]
        )
    if delim is None:
        return pfunc(prefix, data)
    else:
        return pfunc(delim.join(prefix), data)


def type_cond_func(funcs: Dict[Type, Callable], fallback: Callable | None = None):
    """
    Args:
        funcs: dict of type to function
    Returns:
        function that applies the function of the type of the data
    """

    def f(x):
        for tp, func in funcs.items():
            if isinstance(x, tp):
                return func(x)
        if fallback is not None:
            return fallback(x)
        else:
            raise ValueError(f"no function support for type {type(x)}")

    return f


def dict_set_path(dst: dict, path, value, preserve_ret_type: bool = False):
    x = dst
    for p in path[:-1]:
        if p not in x:
            if preserve_ret_type:
                x[p] = type(dst)()
            else:
                x[p] = {}
        x = x[p]
    x[path[-1]] = value
    return dst


def dict_get_path(src: dict, path):
    x = src
    for p in path:
        x = x[p]
    return x


def dict_has_path(src: dict, path):
    x = src
    for p in path:
        if p not in x:
            return False
        x = x[p]
    return True


def dict_apply_split(d: Dict[str, Any], split_func: Callable[[Any], Dict[str, Any]]):
    results = {}
    for key, value in d.items():
        result = split_func(value)
        for k, v in result.items():
            results[k][key] = v
    return results


def dict_apply_reduce(d: List[Dict[str, Any]], reduce_func: Callable[[List[Any]], Any]):
    result = dict()
    for key in d[0].keys():
        result[key] = reduce_func([x_[key] for x_ in d])
    return result

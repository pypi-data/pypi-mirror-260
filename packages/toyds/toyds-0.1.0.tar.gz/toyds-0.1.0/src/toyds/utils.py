import hashlib
import random
import subprocess
from typing import Union

import math

import numpy as np
import torch
import torch.distributed as dist
import hashlib
import os
import pickle
from functools import wraps
import torch.nn as nn
from torch import Tensor


def count_parameters(model: nn.Module, nongrad=False):
    return sum(p.numel() for p in model.parameters() if nongrad or p.requires_grad)


def get_git_commit() -> str:
    """
    https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script
    """
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except subprocess.CalledProcessError:
        commit = "unknown"

    return commit


def get_git_repo() -> str:
    try:
        repo = (
            subprocess.check_output(["git", "remote", "get-url", "origin"])
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        repo = "unknown"

    return repo


def get_git_branch() -> str:
    try:
        branch = (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        branch = "unknown"

    return branch


def might_have_uncommitted_changes():
    try:
        msg = subprocess.check_output(["git", "status", "-s"]).decode().strip()
    except subprocess.CalledProcessError:
        msg = ""

    return len(msg) > 0


def reduce_tensor(tensor, world_size):
    rt = tensor.clone()
    dist.all_reduce(rt, op=dist.ReduceOp.SUM)
    if rt.is_floating_point():
        rt = rt / world_size
    else:
        rt = rt // world_size
    return rt


def seed_all(seed: int):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)


def get_random_states():
    # Get the state of torch, numpy and random libraries random state
    torch_state = torch.get_rng_state()
    np_state = np.random.get_state()
    random_state = random.getstate()
    return torch_state, np_state, random_state


def set_random_states(torch_state, np_state, random_state):
    """Set the state of the libraries"""
    torch.set_rng_state(torch_state)
    np.random.set_state(np_state)
    random.setstate(random_state)


def make_padding_mask(lengths: Tensor) -> Tensor:
    T_max = lengths.max()
    B = lengths.size(0)

    expanded_lengths = torch.arange(T_max).expand(B, T_max).to(lengths)

    return expanded_lengths >= lengths.unsqueeze(1)


def count_nans(x: Tensor):
    nan_mask = torch.isnan(x)
    num_nans = torch.sum(nan_mask).item()
    return num_nans


def prob_mask_like(shape, prob: float, device):
    if prob == 1:
        return torch.ones(shape, device=device, dtype=torch.bool)
    elif prob == 0:
        return torch.zeros(shape, device=device, dtype=torch.bool)
    else:
        return torch.zeros(shape, device=device).float().uniform_(0, 1) < prob


def multinomial(input: Tensor, num_samples: int, replacement=False, *, generator=None):
    """torch.multinomial with arbitrary number of dimensions, and number of candidates on the last dimension.

    Args:
        input (Tensor): The input tensor containing probabilities.
        num_samples (int): Number of samples to draw.
        replacement (bool): Whether to draw with replacement or not.
    Keywords args:
        generator (torch.Generator): A pseudorandom number generator for sampling.
    Returns:
        Tensor: Last dimension contains num_samples indices
            sampled from the multinomial probability distribution
            located in the last dimension of tensor input.
    """
    input_ = input.reshape(-1, input.shape[-1])
    output_ = torch.multinomial(
        input_, num_samples=num_samples, replacement=replacement, generator=generator
    )
    output = output_.reshape(*list(input.shape[:-1]), -1)
    return output


def apply_repetition_penalty(
    prev_ids: Tensor, next_logits: Tensor, repetition_penalty: float = 1.0
):
    score = torch.gather(next_logits, -1, prev_ids)
    score = torch.where(
        score < 0, score * repetition_penalty, score / repetition_penalty
    )
    next_logits = torch.scatter(next_logits, -1, prev_ids, score)
    return next_logits


def sample_top_k(probs: Tensor, k: int) -> Tensor:
    """Sample next token from top K values along the last dimension of the input probs tensor.

    Args:
        probs (Tensor): Input probabilities with token candidates on the last dimension.
        k (int): The k in “top-k”.
    Returns:
        Tensor: Sampled tokens.
    """
    top_k_value, _ = torch.topk(probs, k, dim=-1)
    min_value_top_k = top_k_value[..., [-1]]
    probs *= (probs >= min_value_top_k).float()
    probs.div_(probs.sum(dim=-1, keepdim=True))
    next_token = multinomial(probs, num_samples=1)
    return next_token


def sample_top_p(probs: Tensor, p: float) -> Tensor:
    """Sample next token from top P probabilities along the last dimension of the input probs tensor.

    Args:
        probs (Tensor): Input probabilities with token candidates on the last dimension.
        p (int): The p in “top-p”.
    Returns:
        Tensor: Sampled tokens.
    """
    probs_sort, probs_idx = torch.sort(probs, dim=-1, descending=True)
    probs_sum = torch.cumsum(probs_sort, dim=-1)
    mask = probs_sum - probs_sort > p
    probs_sort *= (~mask).float()
    probs_sort.div_(probs_sort.sum(dim=-1, keepdim=True))
    next_token = multinomial(probs_sort, num_samples=1)
    next_token = torch.gather(probs_idx, -1, next_token)
    return next_token


def sha256(b: Union[float, list, Tensor, str, bytes, np.ndarray]):
    if isinstance(b, (int, list, float)):
        b = str(b)
    if isinstance(b, Tensor):
        b = b.cpu().numpy()
    if isinstance(b, np.ndarray):
        b = b.tostring()
    if type(b) == str:
        b = b.encode()
    if type(b) == bytes:
        return hashlib.sha256(b).hexdigest()
    else:
        raise Exception("Not implemented a method to handle {0}".format(type(b)))

def to_device(obj: [nn.Module, Tensor, list, dict], targets: str | list[str]):
    """
    Takes obj and iterates through the keys putting them on the `device`
    """
    if isinstance(obj, Tensor) or isinstance(obj, nn.Module):
        return obj.to(targets)
    elif isinstance(obj, (list, tuple)):
        return [to_device(item, targets) for item in obj]
    elif isinstance(obj, dict):
        return {key: to_device(value, targets) for key, value in obj.items()}
    else:
        return obj


def hash_arguments(args, kwargs):
    arguments = list(args) + list(kwargs.keys()) + list(kwargs.values())
    return "".join([sha256(b) for b in arguments])

def cache(location=".cache") -> callable:
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            os.makedirs(location, exist_ok=True)
            s = hash_arguments(args, kwargs)
            key = f.__name__ + s
            # Hash the args correctly
            fname = sha256(key)
            fname = os.path.join(location, fname)
            if os.path.exists(fname):
                with open(fname, "rb") as fl:
                    return pickle.load(fl)
            ret = f(*args, **kwargs)
            with open(fname, "wb") as fl:
                pickle.dump(ret, fl)
            return ret

        return wrapper

    return inner_function


def load_what_you_can(checkpoint: dict, model: nn.Module):
    """
    This method takes a checkpoint and loads as many weights from it as possible:

    If they are the same shape, there's nothing to do

    Will load the smallest shape otherwise.
    """
    model_state_dict = model.state_dict()
    checkpoint_state_dict = checkpoint

    for name, param in checkpoint_state_dict.items():
        if name not in model_state_dict:
            print(f"Ignoring parameter '{name}' because it is not found in the model")
            continue

        model_state = model_state_dict[name]
        mshape = model_state.shape
        pshape = param.shape

        if pshape == mshape:
            model_state.copy_(param)
            continue

        if len(pshape) != len(mshape):
            # Completely different shapes so probably unwise to merge
            continue

        min_shape = [
            min(param.shape[i], model_state.shape[i]) for i in range(len(param.shape))
        ]
        print(name, "model:", mshape, "chkpt:", pshape, "loading:", min_shape)
        idxs = torch.meshgrid(*[torch.arange(s) for s in min_shape])
        model_state[tuple(idxs)].copy_(param[tuple(idxs)])

    return model.load_state_dict(model_state_dict)


def dictdiff(maindict: dict, changeddict: dict) -> dict:
    """
    Returns the difference of two dicts
    """
    assert type(maindict) == dict
    assert type(changeddict) == dict
    from copy import deepcopy

    changeddict = deepcopy(changeddict)

    for k in maindict.keys():
        if k not in changeddict:
            continue

        if type(maindict[k]) == dict:
            # Recursive dict difference had no changes either
            dif = dictdiff(maindict[k], changeddict[k])
            changeddict[k] = dif
            if dif == {}:
                del changeddict[k]
        elif maindict[k] == changeddict[k] or (
            maindict[k] is None and not changeddict[k]
        ):
            del changeddict[k]

    return changeddict


def dict_to_strs(d, prefix="") -> str:
    s = []

    for k, v in d.items():
        if type(v) is dict:
            s += dict_to_strs(v, prefix + k + ".")
        else:
            s += [f"{prefix + k}={v}"]

    return s if prefix != "" else "|".join(s)


def human_readable_time(secs: int) -> str:
    days = secs // (24 * 3600)
    hours = (secs % (24 * 3600)) // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"


def human_readable_number(n: int) -> str:
    """Converts long numbers to shorthand:
    1123 -> 1K
    123123 -> 123K
    """
    n = float(n)
    millnames = ["", "K", "M"]
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


def multimap(items: list, func: callable, workers=4, desc=None) -> list:
    """
    Quick and dirty multiprocessing that will return the result of func if it returns None
    """
    from tqdm.contrib.concurrent import process_map

    results = process_map(
        func, items, leave=False, desc=desc, max_workers=workers, total=len(items)
    )
    return list(filter(lambda x: x is not None, results))

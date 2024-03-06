from typing import *
from functools import wraps
from typing_extensions import Self
from copy import deepcopy


def builder_method(mutator_func):
    """
    Turns a function that mutates `self` into a function
    that returns a copy of `self` with those mutations applied.
    """

    @wraps(mutator_func)
    def as_builder_func(self: Self, *args, **kwargs) -> Self:
        safe_copy = deepcopy(self)
        mutator_func(safe_copy, *args, **kwargs)
        return safe_copy

    return as_builder_func

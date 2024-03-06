from typing import *
from .result import Result


def unwrap_nested_result(result: Result) -> Any:
    while hasattr(result, "__result__"):
        result = result.__result__()
    if hasattr(result, "to_wire_format"):
        result = result.to_wire_format()
    return result


def unwrapping_returned_result(func: Callable[[], Result]):
    """
    Decorator which turns the result of a function into the `.__result__` of
    the returned value, if it has one.
    """

    def wrapped(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        return unwrap_nested_result(returned_value)

    return wrapped

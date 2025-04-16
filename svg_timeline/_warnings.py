""" custom implementation of functionality from the warnings standard library,
that is not yet available in all supported python versions
"""
import functools
import warnings
from typing import TypeVar, ParamSpec, Callable

def deprecated(msg: str = "") -> Callable:
    """Use this decorator to mark functions as deprecated.
    Every time the decorated function runs, it will emit  a "deprecation" warning.
    (adapted from https://stackoverflow.com/a/30253848)

    Note: obsolete in python 3.13+
    see https://docs.python.org/3/library/warnings.html#warnings.deprecated
    """
    rT = TypeVar('rT') # return type
    pT = ParamSpec('pT') # parameters type
    def decorator(func: Callable[pT, rT]) -> Callable[pT, rT]:
        @functools.wraps(func)
        def new_func(*args: pT.args, **kwargs: pT.kwargs):
            warnings.warn(f"Avoid using function '{func.__name__}': {msg}",
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return new_func
    return decorator

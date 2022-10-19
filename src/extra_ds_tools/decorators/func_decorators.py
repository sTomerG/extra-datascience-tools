from functools import wraps
from time import time
from typing import Callable, Optional

import pandas as pd
from extra_ds_tools.format import args_and_kwargs_repr
from tabulate import tabulate


def timeit_arg_info_dec(
    function: None = None,
    print_output: bool = True,
    param_info: bool = True,
    round_seconds: Optional[int] = None,
) -> Callable:
    """Decorator that prints the time a function took to execute, and information on its \
        parameters and arguments.

    Parameters
    ----------
    function : None, optional
        For compatability and should always be None, by default None
    print_output : bool, optional
        If True prints the output of the decorated function, by default True
    param_info : bool, optional
        If true prints information about parameters and their arguments, by default True
    round_seconds : Optional[int], optional
        If set rounds the amount of seconds it took the decorated func to exectute, by default None

    Returns
    -------
    Callable
        The decorated function

    Examples
    --------

    >>> @timeit_arg_info_dec
    >>> def illustrate_decorater(a_number: int, text: str, lst: List[int], df: pd.DataFrame, either: bool = True, *args, **kwargs):
    >>>     from time import sleep
    >>>     sleep(1)
    >>>     return "Look how informative!"
    >>>
    >>> illustrate_decorater(42,
                            'Bob',
                            list(range(100)),
                            pd.DataFrame([list(range(1,10))]),
                            either=False,
                            **{'Even': 'this works!'})
    param          type_hint                    default_value    arg_type                     arg_value                 arg_len
    --  -------------  ---------------------------  ---------------  ---------------------------  ------------------------  ---------
    0  a_number       int                                           int                          42
    1  text           str                                           str                          Bob                       3
    2  lst            List[int]                                     list                         [0, 1, 2,  .. 7, 98, 99]  100
    3  df             pandas.core.frame.DataFrame                   pandas.core.frame.DataFrame                            (1, 9)
    4  either         bool                         True             bool                         False
    5  kwarg['Even']                                                str                          this works!               11
    illustrate_decorater() took 1.0047540664672852 seconds to run.
    Returned:
    Look how informative!



    >>> @timeit_arg_info_dec(print_output=False, round_seconds=1)
    >>> def illustrate_decorater(a_number: int, text: str, lst: List[int], df: pd.DataFrame, either: bool = True, *args, **kwargs):
    >>>     from time import sleep
    >>>     sleep(1)
    >>>     return "Look how informative!"
    >>>
    >>> illustrate_decorater(42,
                            'Bob',
                            list(range(100)),
                            pd.DataFrame([list(range(1,10))]),
                            either=False,
                            **{'Even': 'this works!'})
            param          type_hint                    default_value    arg_type                     arg_value                 arg_len
    --  -------------  ---------------------------  ---------------  ---------------------------  ------------------------  ---------
    0  a_number       int                                           int                          42
    1  text           str                                           str                          Bob                       3
    2  lst            List[int]                                     list                         [0, 1, 2,  .. 7, 98, 99]  100
    3  df             pandas.core.frame.DataFrame                   pandas.core.frame.DataFrame                            (1, 9)
    4  either         bool                         True             bool                         False
    5  kwarg['Even']                                                str                          this works!               11
    illustrate_decorater() took 1.0 seconds to run.
    
    See Also
    --------
    Uses:
    :func:`~extra_ds_tools.format.args_and_kwargs_repr`
    """  # noqa

    def _timeit(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if param_info:
                args_and_kwargs = args_and_kwargs_repr(func, *args, **kwargs)
                print(
                    tabulate(
                        pd.DataFrame(args_and_kwargs).fillna(""),
                        headers="keys",
                    )
                )
            start_time = time()
            result = func(*args, **kwargs)
            exec_time = time() - start_time
            if round_seconds:
                exec_time = round(exec_time, round_seconds)
            print(f"\n{func.__name__}() took {exec_time} seconds to run.")
            if print_output:
                print(f"\nReturned:\n{result}")
            return result

        return wrapper

    if function:
        return _timeit(function)
    return _timeit

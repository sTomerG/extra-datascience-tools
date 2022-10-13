import inspect
import re
from inspect import getfullargspec, signature
from typing import Any, Callable, List

import pandas as pd


def args_and_kwargs_repr(func: Callable, *args, **kwargs) -> List[dict]:
    """Returns information about the arguments of a function and \
    its inputted values.

    Parameters
    ----------
    func : Callable
        A function.
    *args : Tuple[Any]
        Positional arguments for the function.
    **kwargs : dict[Any]
        Named key word arguments for the function.

    Returns
    -------
    List[dict]
        Information about the arguments of a function and its inputted values.

    Examples
    --------
    >>> def multiply_two_texts(text1: str, text2: str, n: int = 1):
    >>>     return f"{text1} {text2}" * int
    >>>
    >>> args_and_kwargs_repr(multiply_text, *('arrow','knee'), **{'n': 2})
    [{'param': 'text',
    'type_hint': 'str',
    'default_value': '',
    'arg_type': 'str',
    'arg_value': 'arrow',
    'arg_len': 5},
    {'param': 'n',
    'type_hint': 'int',
    'default_value': 1,
    'arg_type': 'str',
    'arg_value': 'knee',
    'arg_len': 4},
    {'param': "kwarg['p']",
    'arg_type': 'int',
    'arg_value':
    '2',
    'arg_len': ''}]

    >>> def print_every_arg(text: str, *args):
    >>>     print(text)
    >>>     for arg in args:
    >>>         print(arg)
    >>>
    >>> args_and_kwargs_repr(print_every_arg,
                                *('perfect',
                                 2,
                                ['combine', 'with', 'decorator']))
    [{'param': 'text',
    'type_hint': 'str',
    'default_value': '',
    'arg_type': 'str',
    'arg_value': 'perfect',
    'arg_len': 7},
    {'param': 'args[1]',
    'arg_type': 'int',
    'arg_value': '2',
    'arg_len': ''},
    {'param': 'args[2]',
    'arg_type': 'list',
    'arg_value': "['combine' .. ecorator']",
    'arg_len': 3}]

    See Also
    --------
    Uses:
    :func:`~extra_ds_tools.format.arg_info`

    Used by:
    :func:`~extra_ds_tools.decorators.func_decorators.timeit_arg_info_dec`
    """
    args_and_kwargs: List[dict] = []
    sign = signature(func)
    fullargspec = getfullargspec(func)
    for index, arg in enumerate(args):
        args_and_kwargs.append(arg_info(index, arg, sign, fullargspec))

    for key, arg in kwargs.items():
        args_and_kwargs.append(arg_info(key, arg, sign, fullargspec))

    params = [info["param"] for info in args_and_kwargs]
    if len(set(params)) < len(params):
        raise TypeError(
            "Two values were tried to set to the same parameter."
            f"\nFound values for the following parameters:\n{params}"
        )
    return args_and_kwargs


def arg_info(
    key: str,
    arg: Any,
    sign: inspect.signature,
    fullargspec: inspect.FullArgSpec,
) -> dict:
    """Returns a dictionairy with comprehensive information about a single argument.

    Parameters
    ----------
    key : str
        The name of the keyword argument of a function.
    arg : Any
        The argument value passed into the function.
    sign : inspect.signature
        The signature of the function from the inspect module.
    fullargspec : inspect.FullArgSpec
        The FullArgSpec class of the function from the inspect module.

    Returns
    -------
    dict
        A comprehensive dict with information about the argument.

    Examples
    --------
    >>> from inspect import getfullargspec, signature
    >>>
    >>> def multiply_text(text: str, n: int = 1):
    >>>     return text * n
    >>>
    >>> sign = signature(multiply_text)
    >>> fullargspec = getfullargspec(multiply_text)
    >>>
    >>> arg_info(key='text', arg='hello', sign=sign, fullargspec=fullargspec)
    {'param': 'text',
    'type_hint': 'str',
    'default_value': '',
    'arg_type': 'str',
    'arg_value': 'hello',
    'arg_len': 5}

    >>> arg_info(key='n', arg=[1,2], sign=sign, fullargspec=fullargspec)
    {'param': 'n',
    'type_hint': 'int',
    'default_value': 1,
    'arg_type': 'list',
    'arg_value': '[1, 2]',
    'arg_len': 2}

    See Also
    --------
    Uses:
    :func:`~extra_ds_tools.format.class_as_str_repr`
    :func:`~extra_ds_tools.format.truncated_value`
    :func:`~extra_ds_tools.format.make_empty_value_printable`
    """  # noqa
    # store the value and type of the argument
    arg_type: str = class_as_str_repr(arg)
    arg_value: str = truncated_value(arg)

    # check if value has a shape, e.g. with numpy arrays and pandas DataFrames
    try:
        arg_len = str(arg.shape)
    except AttributeError:
        # check if value has a length
        try:
            arg_len = len(arg)
        except TypeError:
            arg_len = ""

    # if the key is in int, it's an *args argument
    if isinstance(key, int):
        func_args = fullargspec.args
        try:
            key = func_args[key]
        except IndexError:
            return {
                "param": f"args[{key}]",
                "arg_type": arg_type,
                "arg_value": arg_value,
                "arg_len": arg_len,
            }
    # if the key is a string but doesn't have a parameter, it's a kwarg
    try:
        param_info = sign.parameters[key]
    except KeyError:
        return {
            "param": f"kwarg['{key}']",
            "arg_type": arg_type,
            "arg_value": arg_value,
            "arg_len": arg_len,
        }
    # get the parameter type hint
    type_hint = class_as_str_repr(param_info.annotation)

    # get the default value of the parameter
    default_value: Any = param_info.default
    default_value = make_empty_value_printable(default_value)

    return {
        "param": key,
        "type_hint": type_hint,
        "default_value": default_value,
        "arg_type": arg_type,
        "arg_value": arg_value,
        "arg_len": arg_len,
    }


def truncated_value(arg: Any, str_limit: int = 20) -> str:
    """Return a string representation of a value, truncated when it's over the str_limit. \
        This is useful for when you don't want to print a long list but would like to see \
            some output.

    Parameters
    ----------
    arg : Any
        Any argument.
    str_limit : int, optional
        The limit of the summary, by default 20

    Returns
    -------
    str
        Arg as a string, truncated so that if it's string representation's length >
        str_limit it's string representation gets truncated.

    Raises
    ------
    ValueError
        If str_limit <= 0

    Examples
    --------
    >>> truncated_value(42)
    42

    Not that interesting. Until we get to strings, lists or other objects with
    a large length.

    >>> truncated_value(list(range(100)), str_limit = 20)
    [0, 1, 2,  .. 7, 98, 99]
    """  # noqa
    if str_limit <= 0:
        raise ValueError(f"str_limit must be > 0, got {str_limit}")
    len_str_repr = len(str(arg))

    # pandas DataFrames and Series have unclear string representation
    # so don't return those
    if len_str_repr <= str_limit and not isinstance(
        arg, (pd.DataFrame, pd.Series)
    ):
        return f"{arg}"
    else:
        if isinstance(arg, (pd.Series, pd.DataFrame)):
            return ""
        else:
            return (
                f"{str(arg)[:int(str_limit/2)]} .. "
                f"{str(arg)[-int(str_limit/2):]}"
            )


def class_as_str_repr(instance: Any) -> str:
    """Returns the class of the instance as a string representation.

    Parameters
    ----------
    instance: Any
        Any instance.

    Returns
    -------
    str
        The string representation of a class.

    Examples
    --------
    >>> class_as_str_repr([3,4])
    'list'

    >>> import numpy as np
    >>> array = np.array([1,2])
    >>> class_as_str_repr(array)
    'numpy.ndarray'

    >>> from typing import Union, List
    >>> class_as_str_repr(Union[List[str], None])
    'Union[List[str], NoneType]'
    """
    # try except because numpy arrays don't accept ==
    try:
        if instance == inspect._empty:
            return ""
    except ValueError:
        pass
    if instance is None:
        return "None"

    # if the instance is from the typing module, just return the string
    # representation as that's more clear
    elif "typing" in str(type(instance)).split(".")[0]:
        return re.sub("typing.", "", str(instance))
    elif isinstance(instance, type):
        return f"""{re.findall("'([^']*)'", str(instance))[0]}"""
    else:
        return f"""{re.findall("'([^']*)'", str(type(instance)))[0]}"""


def make_empty_value_printable(value: Any) -> Any:
    """Makes an empty string or None printable.

    Parameters
    ----------
    value : Any
        Any value.

    Returns
    -------
    Any
        Same as value unless value was an empty string or None.

    Examples
    --------
    Print an empty string will print nothing:

    >>> print('')

    Printing the output of `make_empty_value_printable` shows an empty string.

    >>> print(make_empty_value_printable(''))
    ''

    Printing None will print nothing:

    >>> print(None)

    Printing the output of `make_empty_value_printable` shows None.

    >>> print(make_empty_value_printable(None))
    None
    """
    if value == inspect._empty:
        return ""
    if value == "":
        return "''"
    if value is None:
        return "None"
    return value

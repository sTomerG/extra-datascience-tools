from functools import wraps
from inspect import getfullargspec, signature
from typing import Union

import numpy as np
import pytest
from extra_ds_tools.format import arg_info


def func1(text: str, n: int = 1):
    return


def func2(text: Union[str, int]):
    return


@pytest.mark.parametrize(
    "func, key, arg, expected",
    [
        (
            func1,
            "text",
            "hello",
            {
                "param": "text",
                "type_hint": "str",
                "default_value": "",
                "arg_type": "str",
                "arg_value": "hello",
                "arg_len": 5,
            },
        ),
        (
            func1,
            "n",
            None,
            {
                "param": "n",
                "type_hint": "int",
                "default_value": 1,
                "arg_type": "None",
                "arg_value": "None",
                "arg_len": "",
            },
        ),
        (
            func1,
            "n",
            [1, 2],
            {
                "param": "n",
                "type_hint": "int",
                "default_value": 1,
                "arg_type": "list",
                "arg_value": "[1, 2]",
                "arg_len": 2,
            },
        ),
        (
            func2,
            0,
            np.array([42]),
            {
                "param": "text",
                "type_hint": "Union[str, int]",
                "default_value": "",
                "arg_type": "numpy.ndarray",
                "arg_value": "[42]",
                "arg_len": "(1,)",
            },
        ),
    ],
)
def test_output(func, key, arg, expected):
    sign = signature(func)
    fullargspec = getfullargspec(func)
    output = arg_info(key=key, arg=arg, sign=sign, fullargspec=fullargspec)
    assert output == expected

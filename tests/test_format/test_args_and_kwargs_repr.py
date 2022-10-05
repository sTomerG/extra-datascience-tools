import inspect

import pytest
from extra_ds_tools.format import args_and_kwargs_repr


def func1(text1: str, text2: str, n: int = 1):
    return


def func2(text: str, *args):
    return


@pytest.mark.parametrize(
    "func, args, kwargs, expected",
    [
        (
            func1,
            ("arrow", "knee"),
            {"p": 2},
            [
                {
                    "param": "text1",
                    "type_hint": "str",
                    "default_value": "",
                    "arg_type": "str",
                    "arg_value": "arrow",
                    "arg_len": 5,
                },
                {
                    "param": "text2",
                    "type_hint": "str",
                    "default_value": "",
                    "arg_type": "str",
                    "arg_value": "knee",
                    "arg_len": 4,
                },
                {
                    "param": "kwarg['p']",
                    "arg_type": "int",
                    "arg_value": "2",
                    "arg_len": "",
                },
            ],
        ),
        (
            func2,
            ("perfect", 2, ["combine", "with", "decorator"]),
            {},
            [
                {
                    "param": "text",
                    "type_hint": "str",
                    "default_value": "",
                    "arg_type": "str",
                    "arg_value": "perfect",
                    "arg_len": 7,
                },
                {
                    "param": "args[1]",
                    "arg_type": "int",
                    "arg_value": "2",
                    "arg_len": "",
                },
                {
                    "param": "args[2]",
                    "arg_type": "list",
                    "arg_value": "['combine' .. ecorator']",
                    "arg_len": 3,
                },
            ],
        ),
    ],
)
def test_output(func, args, kwargs, expected):
    assert args_and_kwargs_repr(func, *args, **kwargs) == expected


def test_error_for_same_parameter_values():
    with pytest.raises(TypeError):
        args_and_kwargs_repr(
            func1, *("to param text1"), **{"text1": "going to same parameter"}
        )

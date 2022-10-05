import inspect

import pytest
from extra_ds_tools.format import make_empty_value_printable


@pytest.mark.parametrize(
    "input, expected",
    [
        ("", "''"),
        (None, "None"),
        (inspect._empty, ""),
        (42, 42),
        ([1, 2], [1, 2]),
        ({"hello": "world"}, {"hello": "world"}),
    ],
)
def test_diff_inputs(input, expected):
    assert make_empty_value_printable(input) == expected

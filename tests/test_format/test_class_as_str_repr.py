from typing import List, Union

import numpy as np
import pandas as pd
import pytest
from extra_ds_tools.format import class_as_str_repr


@pytest.mark.parametrize(
    "arg, type_",
    [
        ("1", "str"),
        ([1], "list"),
        (set([1]), "set"),
        ({"1": 1}, "dict"),
        (np.array([1]), "numpy.ndarray"),
        (pd.DataFrame([1]), "pandas.core.frame.DataFrame"),
        (Union[List[str], str], "Union[List[str], str]"),
    ],
)
def test_types(arg, type_):
    assert class_as_str_repr(arg) == type_, f"{arg}, {type_}"

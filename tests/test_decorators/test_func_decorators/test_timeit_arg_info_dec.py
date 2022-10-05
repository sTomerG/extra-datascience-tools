from difflib import SequenceMatcher
from typing import List

import pandas as pd
from extra_ds_tools.decorators.func_decorators import timeit_arg_info_dec


def test_print_output(capfd):
    @timeit_arg_info_dec(round_seconds=1, print_output=False)
    def illustrate_decorater(
        a_number: int,
        text: str,
        lst: List[int],
        df: pd.DataFrame,
        either: bool = True,
        *args,
        **kwargs
    ):
        from time import sleep

        sleep(1)
        return "Look how informative!"

    illustrate_decorater(
        42,
        "Bob",
        list(range(100)),
        pd.DataFrame([list(range(1, 10))]),
        either=False,
        **{"Even": "this works!"}
    )

    expected_output = """    param          type_hint                    default_value    arg_type                     arg_value                 arg_len
--  -------------  ---------------------------  ---------------  ---------------------------  ------------------------  ---------
 0  a_number       int                                           int                          42
 1  text           str                                           str                          Bob                       3
 2  lst            List[int]                                     list                         [0, 1, 2,  .. 7, 98, 99]  100
 3  df             pandas.core.frame.DataFrame                   pandas.core.frame.DataFrame                            (1, 9)
 4  either         bool                         True             bool                         False
 5  kwarg['Even']                                                str                          this works!               11

illustrate_decorater() took 1.0 seconds to run.

'Look how informative!'"""
    out, _ = capfd.readouterr()
    assert (
        SequenceMatcher(a=out.strip(), b=expected_output.strip()).ratio()
        > 0.95
    )

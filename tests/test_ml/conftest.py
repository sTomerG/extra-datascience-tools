import numpy as np
import pandas as pd
import pytest
from numpy.random import default_rng

rng = default_rng()


@pytest.fixture(scope="module")
def normal_with_nans():
    return np.concatenate(
        [
            rng.normal(100, 10, 10).reshape(-1, 1),
            np.full(
                (10, 1),
                np.nan,
            ),
        ]
    )


@pytest.fixture(scope="module")
def normal_with_nans_df():
    return pd.DataFrame(
        {
            "X": np.concatenate(
                [
                    rng.normal(100, 10, 10),
                    np.full(
                        (10,),
                        np.nan,
                    ),
                ]
            )
        }
    )

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
import seaborn as sns
from numpy.random import default_rng

rng = default_rng()


def pytest_configure():
    pytest.CAT_COL = "cat"
    pytest.NUM_COL = "num"


def df_str_num():
    cat = rng.choice(["one", "two", "three"], size=100)
    cat = np.append(cat, np.full(100, [None] * 100))
    num = rng.integers(-1000, 1000, size=100)
    num = np.append(num, np.full(100, [np.nan] * 100))
    rng.shuffle(cat)
    rng.shuffle(num)
    return pd.DataFrame({pytest.CAT_COL: cat, pytest.NUM_COL: num})


def df_cat_num():
    return df_str_num().assign(
        cat=lambda d: d[pytest.CAT_COL].astype("category")
    )


def df_num_num():
    cat = rng.choice([1, 2, 3], size=100)
    cat = np.append(cat, np.full(100, [np.nan] * 100))
    num = rng.integers(-1000, 1000, size=100)
    num = np.append(num, np.full(100, [np.nan] * 100))
    rng.shuffle(cat)
    rng.shuffle(num)
    return pd.DataFrame({pytest.CAT_COL: cat, pytest.NUM_COL: num})


def df_date_num():
    return df_num_num().assign(
        **{
            pytest.CAT_COL: rng.choice(
                [datetime(2022, 1, 1), datetime(2022, 1, 2), np.nan], size=200
            )
        }
    )


@pytest.fixture(params=[df_str_num, df_cat_num, df_num_num, df_date_num])
def dfs(request):
    return request.param


@pytest.fixture(params=[df_str_num, df_cat_num, df_num_num, df_date_num])
def violinplot(request):
    df = request.param()
    fig, ax = plt.subplots()
    sns.violinplot(df, x=pytest.CAT_COL, y=pytest.NUM_COL, ax=ax)
    plt.close("all")
    return fig, ax, df


@pytest.fixture(params=[df_str_num, df_cat_num, df_num_num])
def violinplot_horizontal(request):
    df = request.param()
    fig, ax = plt.subplots()
    sns.violinplot(df, x=pytest.NUM_COL, y=pytest.CAT_COL, ax=ax)
    plt.close("all")
    return fig, ax, df

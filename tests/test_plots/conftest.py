import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
import seaborn as sns
from numpy.random import default_rng

rng = default_rng()


@pytest.fixture
def df_cat_num():
    cat = rng.choice(["one", "two", "three"], size=1000)
    cat = np.append(cat, np.full(100, [None] * 100))
    num = rng.integers(-1000, 1000, size=1000)
    num = np.append(num, np.full(100, [np.nan] * 100))
    rng.shuffle(cat)
    rng.shuffle(num)
    return pd.DataFrame({"cat": cat, "num": num})


@pytest.fixture
def violinplot(df_cat_num):
    fig, ax = plt.subplots()
    sns.violinplot(df_cat_num, x="cat", y="num", ax=ax)
    return fig, ax


@pytest.fixture
def violinplot_horizontal(df_cat_num):
    fig, ax = plt.subplots()
    sns.violinplot(df_cat_num, x="num", y="cat", ax=ax)
    return fig, ax

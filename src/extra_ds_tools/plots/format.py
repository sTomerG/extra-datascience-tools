import re
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd


def add_counts_to_yticks(
    fig: plt.Figure,
    ax: plt.Axes,
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    dropna: bool = False,
) -> Tuple[plt.Figure, plt.Axes]:
    """Adds count statistics to y ticks on a matplotlib Figure.

    Parameters
    ----------
    fig : plt.Figure
        The matplotlib Figure.
    ax : plt.Axes
        The matplotlib Axes to add the count information to.
    df : pd.DataFrame
        The pandas DataFrame with the data of the plot.
    x_col : str
        Name of the column with the values on the x-axis.
    y_col : str
        Name of the column with the values on the y-axis.
    dropna : bool, optional
        Whether to drop count statistics about na values, by default False

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        Returns the Figure and Axes with the added count statistics.

    Examples
    --------
    >>> from numpy.random import default_rng
    >>> import matplotlib.pyplot as plt
    >>> import seaborn as sns
    >>> import pandas as pd
    >>> import numpy as np
    # generate data
    >>> rng = default_rng(42)
    >>> cats = ['Cheetah', 'Leopard', 'Puma']
    >>> cats = rng.choice(cats, size=1000)
    >>> cats = np.append(cats, [None]*102)
    >>> weights = rng.integers(25, 100, size=1000)
    >>> weights = np.append(weights, [np.nan]*100)
    >>> weights = np.append(weights, np.array([125,135]))
    >>> rng.shuffle(cats)
    >>> rng.shuffle(weights)
    >>> df = pd.DataFrame({'cats': cats, 'weights': weights})

    >>> fig, ax = plt.subplots()
    >>> sns.boxplot(data=df, x='weights', y='cats', ax=ax)
    >>> fig, ax = add_counts_to_ticks(fig, ax, df, 'weights', 'cats')
    >>> fig

    .. image:: /images/add_counts_to_yticks.png

    Drop na statistics:

    >>> fig, ax = plt.subplots()
    >>> sns.boxplot(data=df, x='weights', y='cats', ax=ax)
    >>> fig, ax = add_counts_to_yticks(fig, ax, df, 'weights', 'cats', dropna=True)
    >>> fig

    .. image:: /images/add_counts_to_yticks_dropna.png

    """  # noqa
    # get the counts and the relative counts for the y_column

    df = df.copy()
    df[y_col] = df[y_col].astype(str)
    cnts = df[y_col].value_counts(dropna=dropna).to_dict()
    rel_cnts = {
        key: round(value / len(df) * 100, 1) for key, value in cnts.items()
    }

    # calc the nans for the x_col values
    nan_df = df.loc[lambda d: d[x_col].isna()]
    # if no nans set n_nans to 1 to avoide division by zero error
    n_nans = len(nan_df) if len(nan_df) > 0 else 1

    # calculate the x_col nans per y_col value
    nans = nan_df.groupby(y_col).size().to_dict()
    rel_nans = {
        key: round(value / cnts[key] * 100, 1) for key, value in nans.items()
    }

    # create new y_labels in the format:
    # label=(count, rel_to_total%)
    # nan=(count, rel_to_label%)
    # nan_total=(rel_to_total%)
    new_ylabels = []
    for lb in ax.get_yticklabels():
        try:
            _ = cnts[lb.get_text()]
        except KeyError:
            new_ylabels.append("")
        else:
            new_ylabels.append(
                f"{lb.get_text()}=({cnts[lb.get_text()]}, "
                f"{rel_cnts[lb.get_text()]}%)\n"
                f"nan=({nans.get(lb.get_text(),0)}, "
                f"{rel_nans.get(lb.get_text(),0)}%)\n"
                f"nan_total=({round(nans.get(lb.get_text(),0)/n_nans*100,1)}%)"
            )

    if dropna:
        # remove lines that start with nan
        new_ylabels = [
            re.sub(r"nan.*\n*", "", new_label) for new_label in new_ylabels
        ]

    # add total amount of x_nans to x_label
    else:
        ax.set_xlabel(
            f"{ax.get_xlabel()} (nan={len(nan_df)}, "
            f"{round(len(nan_df)/len(df)*100,1)}%)"
        )

    # assign the new ytick labels
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(new_ylabels)

    return fig, ax


def add_counts_to_xticks(
    fig: plt.Figure,
    ax: plt.Axes,
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    dropna: bool = False,
) -> Tuple[plt.Figure, plt.Axes]:
    """Adds count statistics to x ticks on a matplotlib Figure.

    Parameters
    ----------
    fig : plt.Figure
        The matplotlib Figure.
    ax : plt.Axes
        The matplotlib Axes to add the count information to.
    df : pd.DataFrame
        The pandas DataFrame with the data of the plot.
    x_col : str
        Name of the column with the values on the x-axis.
    y_col : str
        Name of the column with the values on the y-axis.
    dropna : bool, optional
        Whether to drop count statistics about na values, by default False

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        Returns the Figure and Axes with the added count statistics.

    Examples
    --------
    >>> from numpy.random import default_rng
    >>> import matplotlib.pyplot as plt
    >>> import seaborn as sns
    >>> import pandas as pd
    >>> import numpy as np
    # generate data
    >>> rng = default_rng(42)
    >>> cats = ['Cheetah', 'Leopard', 'Puma']
    >>> cats = rng.choice(cats, size=1000)
    >>> cats = np.append(cats, [None]*102)
    >>> weights = rng.integers(25, 100, size=1000)
    >>> weights = np.append(weights, [np.nan]*100)
    >>> weights = np.append(weights, np.array([125,135]))
    >>> rng.shuffle(cats)
    >>> rng.shuffle(weights)
    >>> df = pd.DataFrame({'cats': cats, 'weights': weights})

    >>> fig, ax = plt.subplots()
    >>> sns.boxplot(data=df, x='cats', y='weights', ax=ax)
    >>> fig, ax = add_counts_to_xticks(fig, ax, df, 'cats', 'weights')
    >>> fig

    .. image:: /images/add_counts_to_xticks.png

    Drop na statistics:

    >>> fig, ax = plt.subplots()
    >>> sns.boxplot(data=df, x='weights', y='cats', ax=ax)
    >>> fig, ax = add_counts_to_xticks(fig, ax, df, 'weights', 'cats', dropna=True)
    >>> fig

    .. image:: /images/add_counts_to_xticks_dropna.png
    """  # noqa
    # get the counts and the relative counts for the x_column
    df = df.copy()
    df[x_col] = df[x_col].astype(str)
    counts = df[x_col].value_counts(dropna=dropna).to_dict()
    rel_counts = {
        key: round(value / len(df) * 100, 1) for key, value in counts.items()
    }

    # calc the nans for the y_col values
    nan_df = df.loc[lambda d: d[y_col].isna()]
    # if no nans set n_nans to 1 to avoide division by zero error
    n_nans = len(nan_df) if len(nan_df) > 0 else 1

    # calculate the y_col nans per x_col value
    nans = nan_df.groupby(x_col).size().to_dict()
    rel_nans = {
        key: round(value / counts[key] * 100, 1) for key, value in nans.items()
    }

    # create new x_labels in the format:
    # n=count
    # nan=count
    # n%=rel_to_total
    # nan%=rel_to_n
    # nan_t%=rel_to_total
    new_xlabels = []
    for label in ax.get_xticklabels():
        try:
            _ = counts[label.get_text()]
        except KeyError:
            new_xlabels.append("")
        else:
            new_xlabels.append(
                f"""{label.get_text()}
n={counts[label.get_text()]}
nan={nans.get(label.get_text(), 0)}
n%={rel_counts[label.get_text()]}
nan%={rel_nans.get(label.get_text(), 0)}
nan_tot%={round(nans.get(label.get_text(),0)/n_nans*100,1)}"""
            )

    if dropna:
        # remove lines that start with nan
        new_xlabels = [
            re.sub(r"nan.*\n*", "", new_label) for new_label in new_xlabels
        ]
    else:
        # add total amount of y_nans to y_label
        ax.set_ylabel(
            f"{ax.get_ylabel()} (nan={len(nan_df)}, "
            f"{round(len(nan_df)/len(df)*100,1)}%)"
        )

    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(new_xlabels)

    return fig, ax

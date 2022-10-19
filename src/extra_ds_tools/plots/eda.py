from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from extra_ds_tools.transformers.numeric import (
    apply_different_numeric_transformations,
)
from numpy.typing import NDArray


def try_diff_distribution_plots(
    values: NDArray[np.float64],
) -> Tuple[plt.Figure, NDArray[plt.Axes], Dict[str, NDArray[np.float64]]]:
    """Generates the histogram-, probability- and boxplot of \
        different transformations of the values.

    Parameters
    ----------
    values : NDArray[np.float64]
        A list or numpy array of floats.

    Returns
    -------
    Tuple[plt.Figure, NDArray[plt.Axes], Dict[str, NDArray[np.float64]]]
        Returns the figure, the axes with the plots and the transformed values with \
            the transformation title.
        
    Examples
    --------
    >>> from numpy.random import default_rng
    >>> rng = default_rng(42)
    >>> values = rng.pareto(a=100, size=1000)
    >>> fig, axes, transformed_values = try_diff_distribution_plots(values)
    >>> print(transformed_values.keys())
    dict_keys(['untransformed', 'log', 'square-root', 'cube-root', 'reciprocal', 'yeo-johnson', 'box-cox'])
    >>> print(transformed_values['log'][:2])
    [-3.71590427 -3.74494525]
    >>> fig
    
    .. image:: /images/try_diff_distribution_plots.png
    
    See Also
    --------
    Uses:
    :func:`~extra_ds_tools.plots.eda.create_distribution_plots`
    :func:`~extra_ds_tools.transformers.numeric.apply_different_numeric_transformations`
    
    """  # noqa
    transformed_distributions = apply_different_numeric_transformations(values)
    fig, axes = plt.subplots(len(transformed_distributions), 3)
    for index, (transformation_name, values) in enumerate(
        transformed_distributions.items()
    ):
        fig, axes = create_distribution_plots(
            values=values,
            title=transformation_name,
            fig=fig,
            axes=axes,
            row_index=index,
            tight_layout=False,
        )
    fig.set_figheight(len(transformed_distributions) * 3)
    fig.set_figwidth(10)
    fig.tight_layout()
    return fig, axes, transformed_distributions


def create_distribution_plots(
    values: NDArray[np.float64],
    title: str = "",
    fig: plt.Figure = None,
    axes: NDArray[plt.Axes] = None,
    row_index: int = 0,
    hist_bins: int = 30,
    tight_layout: bool = True,
) -> Tuple[plt.Figure, NDArray[plt.Axes]]:
    """Adds a histogram-, probabilty and boxplot to the axes.

    Parameters
    ----------
    values : NDArray[np.float64]
        Values to create the plots from.
    title : str, optional
        Title of the plots, by default ""
    fig : plt.Figure, optional
        A matplotlib Figure, by default None
    axes : NDArray[plt.Axes], optional
        Axes to draw to plots on, by default None
    row_index : int, optional
        The row index of the axes for the plots to be added to, by default 0
    hist_bins : int, optional
        Amount of bins for the histogram, by default 30
    tight_layout : bool, optional
        Automatically prettifies the layout of the Figure. Not recommended \
            when give a Figure and Axes as arguments, by default True

    Returns
    -------
    Tuple[plt.Figure, NDArray[plt.Axes]]
        The figure and the axes, with a histogram-, probability- and boxplot.

    Examples
    --------
    >>> fig, axes = create_distribution_plots(list(range(90)))
    >>> fig

    .. image:: /images/create_distribution_plots.png
    
    >>> fig, axes = create_distribution_plots(list(range(0,90,3)), title="<title>", hist_bins=3)
    >>> fig
    
    .. image:: /images/create_distribution_plots_title.png
    
    """  # noqa
    if not fig or not axes.any():
        fig, axes = plt.subplots(1, 3)
        fig.set_figheight(5)
        fig.set_figwidth(10)
        axes = axes.reshape(1, 3)

    sns.histplot(values, bins=hist_bins, ax=axes[row_index, 0])
    axes[row_index, 0].set_title(f"Histogram {title}")

    stats.probplot(values, dist="norm", plot=axes[row_index, 1])
    axes[row_index, 1].set_title(f"Probplot {title}")

    sns.boxplot(y=values, ax=axes[row_index, 2])
    axes[row_index, 2].set_title(f"Boxplot {title}")

    if tight_layout:
        fig.tight_layout()
    return fig, axes

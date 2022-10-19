from typing import Dict

import numpy as np
import scipy.stats as stats
from numpy.typing import NDArray


def apply_different_numeric_transformations(
    values: NDArray[np.float64],
) -> Dict[str, NDArray[np.float64]]:
    """Applies different transformations to a list with numbers.

    Parameters
    ----------
    values : NDArray[np.float64]
        List or numpy array with numeric values.

    Returns
    -------
    Dict[str, NDArray[np.float64]]
        Dictionairy with key is the name of the transformation and value \
            is a numpy array with the transformed values.

    Examples
    --------
    >>> apply_different_numeric_transformations([2,3,4])
    {'untransformed': array([2., 3., 4.]),
    'log': array([0.69314718, 1.09861229, 1.38629436]),
    'square-root': array([1.41421356, 1.73205081, 2.]),
    'cube-root': array([1.25992105, 1.44224957, 1.58740105]),
    'reciprocal': array([0.5, 0.33333333, 0.25]),
    'yeo-johnson': array([1.55048017, 2.1536574 , 2.69802755]),
    'box-cox': array([0.85657355, 1.54652658, 2.14655732])}
    """

    values = np.array(values).astype(float)

    numpy_transformers = [
        (np.log, "log"),
        (np.sqrt, "square-root"),
        (np.cbrt, "cube-root"),
        (np.reciprocal, "reciprocal"),
    ]

    stats_transformers = [
        (stats.yeojohnson, "yeo-johnson"),
        (stats.boxcox, "box-cox"),
    ]

    transformed_data = {"untransformed": values}

    for transformer, transformer_name in numpy_transformers:
        transformed_data[transformer_name] = transformer(values)

    for transformer, transformer_name in stats_transformers:
        try:
            transformed_values, _ = transformer(values)
        except (ValueError, IndexError):
            pass
        else:
            transformed_data[transformer_name] = transformed_values

    return transformed_data

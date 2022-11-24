from itertools import product
from typing import List

from sklearn.model_selection import GridSearchCV


def filter_tried_params(
    gridsearchcv: GridSearchCV,
    tried_gridsearches: List[GridSearchCV],
) -> List[dict]:
    """Filters out previously tried parameters for a scikit-learn gridsearch if the \
        model otherwise is identically the same.

    Parameters
    ----------
    gridsearchcv : GridSearchCV
        The gridsearch model you want to run.
    tried_gridsearches : List[GridSearchCV]
        The previous gridsearch models you've already run.

    Returns
    -------
    List[dict]
        A parameter grid without previously tried parameters.
        
    Examples
    --------
    Click `here. <https://extra-datascience-tools.readthedocs.io/en/latest/notebooks/tutorial.html#filter_tried_params>`_
    """  # noqa

    tried_params = []
    for prev_gs in tried_gridsearches:

        # only compare param grids if the estimator steps are identical
        if str(gridsearchcv.get_params()["estimator__steps"]) == str(
            prev_gs.get_params()["estimator__steps"]
        ):
            # if the param grid is a dictionairy
            if isinstance(prev_gs.param_grid, dict):
                keys, values = zip(*prev_gs.param_grid.items())
                tried_params += [dict(zip(keys, v)) for v in product(*values)]

            # if the param grid is a list of dictionaries
            elif isinstance(prev_gs.param_grid, list):
                for dict_ in prev_gs.param_grid:
                    keys, values = zip(*dict_.items())
                    tried_params += [
                        dict(zip(keys, v)) for v in product(*values)
                    ]

    # remove duplicates
    tried_params = [
        i for n, i in enumerate(tried_params) if i not in tried_params[n + 1 :]
    ]

    # generate the new params
    if isinstance(gridsearchcv.param_grid, dict):
        keys, values = zip(*gridsearchcv.param_grid.items())
        new_params = [
            dict(zip(keys, v))
            for v in product(*values)
            if dict(zip(keys, v)) not in tried_params
        ]

    elif isinstance(gridsearchcv.param_grid, list):
        new_params = []
        for dict_ in gridsearchcv.param_grid:
            keys, values = zip(*dict_.items())
            new_params += [
                dict(zip(keys, v))
                for v in product(*values)
                if dict(zip(keys, v)) not in tried_params
            ]

    # remove duplicates
    new_params = [
        i for n, i in enumerate(new_params) if i not in new_params[n + 1 :]
    ]

    # return new_params as a list with dictionaires
    return list(
        map(lambda d: dict((k, [v]) for k, v in d.items()), new_params)
    )

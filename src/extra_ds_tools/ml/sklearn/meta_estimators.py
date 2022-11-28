from typing import Any, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class EstimatorSwitch(TransformerMixin, BaseEstimator):
    """A Meta Estimator that can turn on or off an estimator \
        in a scikit-learn Pipeline.

    Parameters
    ----------
    estimator : Any
        The estimator to turn on or off.
    apply : bool
        To apply the estimator, by default True.
        
    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.pipeline import make_pipeline
    >>> from sklearn.impute import SimpleImputer, MissingIndicator
    >>> from extra_ds_tools.ml.sklearn.meta_estimators import EstimatorSwitch
    >>> X = np.array([np.nan, 10] * 2).reshape(-1, 1)
    >>> # The SimpleImputer should transform the nans to the mean, which is 10.
    >>> pipeline = make_pipeline(EstimatorSwitch(SimpleImputer(), apply=False))
    >>> print(pipeline.fit_transform(X))
    [[nan]
    [10.]
    [nan]
    [10.]]
    """  # noqa

    def __init__(self, estimator: Any, *, apply: bool = True):
        self.estimator = estimator
        self.apply = apply

    def fit(
        self,
        X: Union[pd.DataFrame, pd.Series, np.array],
        y: Optional[Union[pd.Series, np.array]] = None,
        **fit_params
    ):
        """Fits the estimator on the data if self.apply == True.

        Parameters
        ----------
        X : Union[pd.DataFrame, pd.Series, np.array]
            Train data.
        y : Optional[Union[pd.Series, np.array]], optional
            Target data, by default None.

        Returns
        -------
        EstimatorSwitch
            EstimatorSwitch with a fitted estimator if self.apply == True.
        """
        if self.apply:
            return self.estimator.fit(X, y, **fit_params)
        return self

    def transform(
        self,
        X: Union[pd.DataFrame, pd.Series, np.array],
        y: Optional[Union[pd.Series, np.array]] = None,
        **fit_params
    ):
        """Returns the transformed X if self.apply == True.

        Parameters
        ----------
         X : Union[pd.DataFrame, pd.Series, np.array]
             Train data.
         y : Optional[Union[pd.Series, np.array]], optional
             Target data, by default None.

        Returns
        -------
        Union[pd.DataFrame, pd.Series, np.array]
             Transformed X.
        """
        if self.apply:
            return self.estimator.transform(X, y, **fit_params)
        return X

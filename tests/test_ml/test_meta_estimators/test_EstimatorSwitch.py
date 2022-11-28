import numpy as np
from extra_ds_tools.ml.sklearn.meta_estimators import EstimatorSwitch
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline


def test_with_apply_numpy(normal_with_nans):
    pipeline = make_pipeline(EstimatorSwitch(SimpleImputer()))
    assert np.isnan(pipeline.fit_transform(normal_with_nans)).sum() == 0


def test_without_apply_numpy(normal_with_nans):
    pipeline = make_pipeline(EstimatorSwitch(SimpleImputer(), apply=False))
    assert np.isnan(pipeline.fit_transform(normal_with_nans)).sum() > 0


def test_with_apply_df(normal_with_nans_df):
    pipeline = make_pipeline(EstimatorSwitch(SimpleImputer()))
    assert np.isnan(pipeline.fit_transform(normal_with_nans_df)).sum() == 0


def test_without_apply_df(normal_with_nans_df):
    pipeline = make_pipeline(EstimatorSwitch(SimpleImputer(), apply=False))
    assert (
        pipeline.fit_transform(normal_with_nans_df).isna().sum().values[0] > 0
    )

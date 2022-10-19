import pytest
from extra_ds_tools.plots.eda import try_diff_distribution_plots
from matplotlib.pyplot import subplots
from numpy.random import default_rng

rng = default_rng()


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_with_floats():
    floats = rng.uniform(-1000, 1000, 1000)
    try_diff_distribution_plots(floats)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_with_ints():
    ints = rng.integers(-1000, 1000, 1000)
    try_diff_distribution_plots(ints)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_output_types():
    ints = rng.integers(-1000, 1000, 1000)
    fig, axes, value_dict = try_diff_distribution_plots(ints)
    fig2, axes2 = subplots(1, 3)
    assert isinstance(fig, type(fig2))
    assert isinstance(axes, type(axes2))
    assert isinstance(value_dict, dict)

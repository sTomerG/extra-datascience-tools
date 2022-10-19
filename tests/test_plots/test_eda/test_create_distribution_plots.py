from extra_ds_tools.plots.eda import create_distribution_plots
from numpy.random import default_rng

rng = default_rng()


def test_for_floats():
    floats = rng.uniform(-1000, 1000, 1000)
    print(floats)
    create_distribution_plots(floats)


def test_for_ints():
    ints = rng.integers(-1000, 1000, 1000)
    print(ints)
    create_distribution_plots(ints)

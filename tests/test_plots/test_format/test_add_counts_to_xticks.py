import matplotlib.pyplot as plt
import pytest
from extra_ds_tools.plots.format import add_counts_to_xticks


def test_no_errors(violinplot):
    fig, ax, df = violinplot
    add_counts_to_xticks(fig, ax, df, pytest.CAT_COL, pytest.NUM_COL)
    plt.close("all")


def test_no_nans(violinplot):
    fig, ax, df = violinplot
    fig, ax = add_counts_to_xticks(
        fig, ax, df, pytest.CAT_COL, pytest.NUM_COL, dropna=True
    )
    x_label_texts = " ".join([lbl.get_text() for lbl in ax.get_xticklabels()])
    assert "nan" not in x_label_texts
    plt.close("all")

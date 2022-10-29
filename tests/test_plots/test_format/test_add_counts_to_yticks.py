import matplotlib.pyplot as plt
import pytest
from extra_ds_tools.plots.format import add_counts_to_yticks


def test_no_errors(violinplot_horizontal):
    fig, ax, df = violinplot_horizontal
    add_counts_to_yticks(fig, ax, df, pytest.NUM_COL, pytest.CAT_COL)
    plt.close("all")


def test_no_nans(violinplot_horizontal):
    fig, ax, df = violinplot_horizontal
    fig, ax = add_counts_to_yticks(
        fig, ax, df, pytest.NUM_COL, pytest.CAT_COL, dropna=True
    )
    y_label_texts = " ".join([lbl.get_text() for lbl in ax.get_yticklabels()])
    assert "nan" not in y_label_texts
    plt.close("all")

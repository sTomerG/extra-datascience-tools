import matplotlib.pyplot as plt
import pytest
from extra_ds_tools.plots.eda import stripboxplot


@pytest.mark.parametrize("horizontal", [True, False])
@pytest.mark.parametrize("dropna", [True, False])
@pytest.mark.parametrize("count_info", [True, False])
@pytest.mark.parametrize("show_outliers", [True, False])
@pytest.mark.parametrize("show_legend", [True, False])
@pytest.mark.parametrize("sort_by_median", [True, False])
def test_no_errors(
    dfs,
    horizontal,
    dropna,
    count_info,
    show_outliers,
    show_legend,
    sort_by_median,
):
    stripboxplot(
        dfs(),
        pytest.CAT_COL,
        pytest.NUM_COL,
        horizontal,
        dropna,
        count_info,
        show_outliers,
        show_legend,
        sort_by_median,
    )
    plt.close("all")


@pytest.mark.parametrize("count_info", [True, False])
@pytest.mark.parametrize("show_outliers", [True, False])
@pytest.mark.parametrize("show_legend", [True, False])
@pytest.mark.parametrize("sort_by_median", [True, False])
def test_dropna(dfs, count_info, show_outliers, show_legend, sort_by_median):
    # test for x labels
    _, ax = stripboxplot(
        dfs(),
        pytest.CAT_COL,
        pytest.NUM_COL,
        False,
        True,
        count_info,
        show_outliers,
        show_legend,
        sort_by_median,
    )
    xlabel_texts = " ".join([lbl.get_text() for lbl in ax.get_xticklabels()])
    assert "nan" not in xlabel_texts
    plt.close("all")

    # test for y labels
    _, ax = stripboxplot(
        dfs(),
        pytest.CAT_COL,
        pytest.NUM_COL,
        True,
        True,
        count_info,
        show_outliers,
        show_legend,
        sort_by_median,
    )
    ylabel_texts = " ".join([lbl.get_text() for lbl in ax.get_yticklabels()])
    assert "nan" not in ylabel_texts
    plt.close("all")

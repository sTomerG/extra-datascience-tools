import matplotlib.pyplot as plt
import pytest
from extra_ds_tools.plots.eda import stripboxplot


@pytest.mark.parametrize("horizontal", [True, False])
@pytest.mark.parametrize("dropna", [True, False])
@pytest.mark.parametrize("count_info", [True, False])
@pytest.mark.parametrize("show_outliers", [True, False])
@pytest.mark.parametrize("show_legend", [True, False])
def test_no_errors(
    df_cat_num,
    horizontal,
    dropna,
    count_info,
    show_outliers,
    show_legend,
):
    stripboxplot(
        df_cat_num,
        "cat",
        "num",
        horizontal,
        dropna,
        count_info,
        show_outliers,
        show_legend,
    )
    plt.close()


@pytest.mark.parametrize("count_info", [True, False])
@pytest.mark.parametrize("show_outliers", [True, False])
@pytest.mark.parametrize("show_legend", [True, False])
def test_dropna(df_cat_num, count_info, show_outliers, show_legend):
    # test for x labels
    _, ax = stripboxplot(
        df_cat_num,
        "cat",
        "num",
        False,
        True,
        count_info,
        show_outliers,
        show_legend,
    )
    xlabel_texts = " ".join([lbl.get_text() for lbl in ax.get_xticklabels()])
    assert "nan" not in xlabel_texts

    # test for y labels
    _, ax = stripboxplot(
        df_cat_num,
        "cat",
        "num",
        True,
        True,
        count_info,
        show_outliers,
        show_legend,
    )
    ylabel_texts = " ".join([lbl.get_text() for lbl in ax.get_yticklabels()])
    assert "nan" not in ylabel_texts
    plt.close()

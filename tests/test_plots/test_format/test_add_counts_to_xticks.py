from extra_ds_tools.plots.format import add_counts_to_xticks


def test_no_errors(df_cat_num, violinplot):
    fig, ax = violinplot
    add_counts_to_xticks(fig, ax, df_cat_num, "cat", "num")


def test_no_nans(df_cat_num, violinplot):
    fig, ax = violinplot
    fig, ax = add_counts_to_xticks(
        fig, ax, df_cat_num, "cat", "num", dropna=True
    )
    x_label_texts = " ".join([lbl.get_text() for lbl in ax.get_xticklabels()])
    assert "nan" not in x_label_texts

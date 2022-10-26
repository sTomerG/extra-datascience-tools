from extra_ds_tools.plots.format import add_counts_to_yticks


def test_no_errors(df_cat_num, violinplot_horizontal):
    fig, ax = violinplot_horizontal
    add_counts_to_yticks(fig, ax, df_cat_num, "num", "cat")


def test_no_nans(df_cat_num, violinplot_horizontal):
    fig, ax = violinplot_horizontal
    fig, ax = add_counts_to_yticks(
        fig, ax, df_cat_num, "num", "cat", dropna=True
    )
    y_label_texts = " ".join([lbl.get_text() for lbl in ax.get_yticklabels()])
    assert "nan" not in y_label_texts

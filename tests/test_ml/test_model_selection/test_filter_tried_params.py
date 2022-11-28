import pytest
from extra_ds_tools.ml.sklearn.model_selection import filter_tried_params


@pytest.mark.parametrize(
    "gridsearches",
    [
        "gridsearchcvs_tree_dict",
        "gridsearchcvs_tree_list",
        "gridsearchcvs_tree_dictlist",
        "gridsearchcvs_tree_listdict",
        "gridsearchcvs_tree_dict_pipeline",
        "gridsearchcvs_tree_list_pipeline",
        "gridsearchcvs_tree_dictlist_pipeline",
        "gridsearchcvs_tree_listdict_pipeline",
    ],
)
def test_filter_tried_params_dict(gridsearches, request):
    new_gridsearch, *tried_gridsearches = request.getfixturevalue(gridsearches)
    new_params = filter_tried_params(new_gridsearch, tried_gridsearches)
    assert len(new_params) == 2

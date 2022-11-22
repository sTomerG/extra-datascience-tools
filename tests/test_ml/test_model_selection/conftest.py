import pytest
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor


@pytest.fixture(scope="module")
def gridsearchcvs_tree_dict():
    trees = []
    model = make_pipeline(DecisionTreeRegressor())
    for i in range(1, 4):
        param_grid = {
            "decisiontreeregressor__max_depth": [i, i + 1],
            "decisiontreeregressor__splitter": ["best", "random"],
        }
        clf = GridSearchCV(model, param_grid)
        trees.append(clf)
    return trees


@pytest.fixture(scope="module")
def gridsearchcvs_tree_list():

    model = make_pipeline(DecisionTreeRegressor())
    trees = []
    param_grids = [
        [
            {
                "decisiontreeregressor__max_depth": [i, i + 1],
                "decisiontreeregressor__splitter": ["best"],
            },
            {
                "decisiontreeregressor__max_depth": [i, i + 1],
                "decisiontreeregressor__splitter": ["random"],
            },
        ]
        for i in range(1, 4)
    ]
    for grid in param_grids:
        clf = GridSearchCV(model, grid)
        trees.append(clf)
    return trees


@pytest.fixture(scope="module")
def gridsearchcvs_tree_dictlist():

    model = make_pipeline(DecisionTreeRegressor())
    trees = []
    param_grids = [
        {
            "decisiontreeregressor__max_depth": [1, 2],
            "decisiontreeregressor__splitter": ["best", "random"],
        }
    ]
    param_grids += [
        [
            {
                "decisiontreeregressor__max_depth": [i, i + 1],
                "decisiontreeregressor__splitter": ["best"],
            },
            {
                "decisiontreeregressor__max_depth": [i, i + 1],
                "decisiontreeregressor__splitter": ["random"],
            },
        ]
        for i in range(2, 4)
    ]
    for grid in param_grids:
        clf = GridSearchCV(model, grid)
        trees.append(clf)
    return trees


@pytest.fixture(scope="module")
def gridsearchcvs_tree_listdict():

    model = make_pipeline(DecisionTreeRegressor())
    trees = []
    param_grids = [
        [
            {
                "decisiontreeregressor__max_depth": [1, 2],
                "decisiontreeregressor__splitter": ["best"],
            },
            {
                "decisiontreeregressor__max_depth": [1, 2],
                "decisiontreeregressor__splitter": ["random"],
            },
        ]
    ]
    param_grids += [
        {
            "decisiontreeregressor__max_depth": [i, i + 1],
            "decisiontreeregressor__splitter": ["best", "random"],
        }
        for i in range(2, 4)
    ]
    for grid in param_grids:
        clf = GridSearchCV(model, grid)
        trees.append(clf)
    return trees

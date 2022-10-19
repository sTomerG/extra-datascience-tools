import hypothesis.strategies as st
import pytest
from extra_ds_tools.transformers.numeric import (
    apply_different_numeric_transformations,
)
from hypothesis import given
from numpy import ndarray


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@given(input=st.lists(st.floats()))
def test_for_floats(input):
    apply_different_numeric_transformations(input)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@given(input=st.lists(st.integers()))
def test_for_ints(input):
    apply_different_numeric_transformations(input)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@given(input=st.lists(st.floats()))
def test_output_type(input):
    for text, array in apply_different_numeric_transformations(input).items():
        assert isinstance(array, ndarray)
        assert isinstance(text, str)

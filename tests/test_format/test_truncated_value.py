import inspect

import hypothesis.strategies as st
import pytest
from extra_ds_tools.format import truncated_value
from hypothesis import HealthCheck, assume, given, settings


@pytest.fixture
def default_str_limit():
    sign = inspect.signature(truncated_value)
    return sign.parameters["str_limit"].default


@given(
    arg=st.one_of(
        st.complex_numbers(),
        st.text(),
        st.dates(),
        st.datetimes(),
        st.dictionaries(
            keys=st.text(max_size=5), values=st.text(max_size=5), max_size=10
        ),
        st.lists(elements=st.text(max_size=5), max_size=5),
    )
)
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
def test_short_arguments(arg, default_str_limit):
    assume(len(str(arg)) <= default_str_limit)
    assert truncated_value(arg) == str(arg)


@given(
    arg=st.one_of(
        st.dictionaries(
            keys=st.text(max_size=5), values=st.text(max_size=5), min_size=60
        ),
        st.lists(elements=st.text(min_size=1, max_size=5), min_size=60),
    ),
    str_limit=st.integers(min_value=1, max_value=100),
)
def test_long_arguments(arg, str_limit):
    assume(len(str(arg)) > str_limit)
    output = truncated_value(arg, str_limit=str_limit)
    assert str(arg)[: int(str_limit / 2)] in output
    assert str(arg)[-int(str_limit / 2) :] in output


@given(str_limit=st.integers(max_value=0))
def test_negative_str_limit(str_limit):
    with pytest.raises(ValueError):
        truncated_value("", str_limit=str_limit)

import pytest
from tomodachi_core.tomodachi.services import PandasService
from tomodachi_core.common_types.result import Ok, Err, Result
from tomodachi_core.common_types.option import Option, Some

@pytest.fixture()
def pandas_service():
    service = PandasService()
    return service


def test_preprocess_none(pandas_service):
    df = pandas_service.get_mock_dataframe
    pandas_service.update_dataframe(df)
    df = pandas_service.get_df()

    # we are certain that
    assert df is not None

    some_df = pandas_service.preprocess_df(df.unwrap(), None, None)
    assert some_df.is_some()


# Testing new type: Option

x: Option[int] = Some(2)
assert x.is_some_and(lambda k: k > 1) == True
assert x.is_some_and(lambda k: k > 2) == False

y: Option[str] = Some("ownership")
assert y.is_some_and(lambda s: len(s) > 1) == True

# map example
mapped_x = x.map(lambda val: val * 2)
assert mapped_x == Some(4)

# filter example
filtered_x = x.filter(lambda val: val % 2 == 0) # 2 is even
assert filtered_x == Some(2)

# unwrap and expect
value_from_some = x.unwrap()
value_from_expect = x.expect("Should not fail")

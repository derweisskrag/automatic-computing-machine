import pytest
from tomodachi_core.tomodachi.services import PandasService
from tomodachi_core.common_types.result import Err
from pandas import DataFrame

@pytest.fixture()
def pandas_service():
    service = PandasService()
    return service


def test_if_dataframe(pandas_service):
    df = pandas_service.get_mock_dataframe
    assert pandas_service.is_dataframe(df).unwrap_or(False) == True


def test_get_mock_data(pandas_service):
    df = pandas_service.get_mock_dataframe
    assert df is not None, f"We got the mock dataframe"

    # test the columns
    cols = df.columns.tolist()
    expected_columns = [
        "name",
        "age",
        "profession",
        "salary",
        "hobby",
        "country",
        "phone",
    ]


    assert all(
        col in expected_columns
        for col in cols
    ), f"Unexpected columns found: {set(cols) - set(expected_columns)}"

    # test the shape of the df
    expected_shape = (5, 7)
    actual_shape = df.shape
    assert actual_shape == expected_shape, f"Expected shape {expected_shape}, but got {actual_shape}"

    # test the content
    assert df.loc[df['name'] == "Sakura", 'country'].item() == "Japan", "Sakura should be from Japan"


    # test if it is cached
    assert pandas_service.get_mock_dataframe is pandas_service.get_mock_dataframe



def test_mock_dataframe_types(pandas_service):
    expected_dtypes = {
        "name": object,
        "age": int,
        "profession": object,
        "salary": object,
        "hobby": object,
        "country": object,
        "phone": object,
    }

    df = pandas_service.get_mock_dataframe
    for col, dtype in expected_dtypes.items():
        assert df[col].dtype == dtype, f"Expected dtype {dtype} for '{col}', got {df[col].dtype}"


def test_monkey(monkeypatch):
    def get_mock_dataframe(self):
        return Err("Failed to produce data...")

    monkeypatch.setattr(PandasService, 'get_mock_dataframe', get_mock_dataframe)
    service = PandasService()
    df = service.get_mock_dataframe().unwrap_or(DataFrame({"cities": ["New York", "London", "Tokyo"], "countries": ["USA", "England", "Japan"]}))
    assert not df.empty

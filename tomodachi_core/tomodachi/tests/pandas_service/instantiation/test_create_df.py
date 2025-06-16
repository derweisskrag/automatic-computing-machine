import pytest
from tomodachi_core.tomodachi.services import PandasService
from tomodachi_core.common_types.result import Ok, Err, Result
import pandas as pd
import numpy as np

@pytest.fixture()
def pandas_service():
    service = PandasService()
    return service


def test_create_df(pandas_service):
    response = pandas_service.from_dict({
        "Timestamp": ['2025/07/01 10:00:00', '2021/11/03 15:45:00', '2017/05/27 13:10:50'],
        "name": ["Alice", "Bob", "John"],
        "age": [21, 38, 27],
        "country": ["USA", "London", np.nan],
    })

    df = response.unwrap()
    assert pd.api.types.is_datetime64_ns_dtype(df["Timestamp"]), "Timestamp must be datetime"
    assert df.isna().sum().sum() == 0


def test_empty_path():
    """
    This test tests if the functionality of the PandasService persists when the path is
    None. Usually we can use it to load the data.
    """
    service = PandasService("")
    assert service.path == ""
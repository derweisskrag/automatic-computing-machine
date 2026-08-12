import pytest
from tomodachi_core.tomodachi.services import PandasService
from numpy import nan
from pandas import DataFrame

@pytest.fixture()
def pandas_service():
    service = PandasService()
    return service


def test_instantiation_from_dict(benchmark, pandas_service):
    test_data = {
        "Timestamp": ['2025/07/01 10:00:00', '2021/11/03 15:45:00', '2017/05/27 13:10:50'],
        "name": ["Alice", "Bob", "John"],
        "age": [21, 38, 27],
        "country": ["USA", "London", nan]
    }


    result = benchmark(pandas_service.from_dict, test_data)
    assert result.is_ok()
    assert isinstance(result.unwrap(), DataFrame)
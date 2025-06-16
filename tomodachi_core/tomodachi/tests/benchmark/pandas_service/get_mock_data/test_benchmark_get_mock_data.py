import pytest
from tomodachi_core.tomodachi.services import PandasService
from pandas import DataFrame

@pytest.fixture()
def pandas_service():
    service = PandasService()
    return service

def test_get_mock_dataframe_benchmark(benchmark, pandas_service):
    result = benchmark(lambda: pandas_service.get_mock_dataframe)
    assert isinstance(result, DataFrame)
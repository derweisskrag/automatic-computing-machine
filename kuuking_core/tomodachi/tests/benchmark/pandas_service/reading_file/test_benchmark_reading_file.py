import pytest

from tomodachi_core.tomodachi.services import PandasService
from tomodachi_core.config_development.config import TEST_PATH

@pytest.fixture()
def pandas_service():
    service = PandasService(TEST_PATH + "test_file.csv")
    service.load_csv_data()
    return service

def test_load_csv_benchmark(benchmark, pandas_service):
    benchmark(pandas_service.load_csv_data)
"""
This module contains unit tests for the PandasService class.
It tests the functionality of reading a CSV file and loading it into a DataFrame.
"""

import pytest
from tomodachi_core.common_types.result import Err
from tomodachi_core.tomodachi.services import PandasService
from tomodachi_core.config_development.config import TEST_PATH 

@pytest.fixture()
def pandas_service():
    service = PandasService(TEST_PATH + "test_file.csv")
    service.load_csv_data()
    return service

# Test for reading 'test_file.csv' file
def test_read_file(pandas_service):
    assert pandas_service.get_df().unwrap() is not None, "Data should not be None after loading CSV file."
    assert len(pandas_service.df) > 0, "DataFrame should not be empty after loading CSV file."

    # compare the data
    expected_columns = [5.2, 6.3, 5.2, 7.1, 6.3, 4.8]
    actual = pandas_service.df['wind_speed'].tolist()
    assert actual == expected_columns, f"Expected {expected_columns}, but got {actual}."
    

# Test for reading a CSV file using context manager
def test_read_file_context_manager(pandas_service):
    with pandas_service.connection() as df:
        assert df is not None, "Data should not be None after loading CSV file."
        assert len(df) > 0, "DataFrame should not be empty after loading CSV file."

        # compare the data
        expected_columns = [5.2, 6.3, 5.2, 7.1, 6.3, 4.8]
        actual = df['wind_speed'].tolist()
        assert actual == expected_columns, f"Expected {expected_columns}, but got {actual}."


# Test for reading a CSV file with an invalid path
def test_read_file_invalid_path():
    service = PandasService("invalid_path.csv")
    match service.load_csv_data():
        case Err(error=error) if isinstance(error, FileNotFoundError):
            assert True, "FileNotFoundError raised as expected."
        case _:
            assert False, "Expected FileNotFoundError, but got a different error."


def test_read_file_wrong_path():
    with pytest.raises(ValueError, match="Please, provide valid path!"):
        service = PandasService(123) # not string
    
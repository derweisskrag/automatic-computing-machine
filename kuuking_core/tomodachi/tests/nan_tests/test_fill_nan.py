import unittest
import pandas as pd

# import tomodachi module
from tomodachi_core.tomodachi.utils.data_utils import analyze_and_fill_missing_values

# import test data
# this failed to import, so we moved the test data to the same directory as the test file


from tomodachi_core.tomodachi.tests.testdata import (
    data_with_nan,
    data_without_nan,
    data_with_multiple_col_nan,
    data_with_no_numerical,
    expected_data_with_nan,
    expected_data_without_nan,
    expected_data_with_multiple_col_nan
)

class TestAnalyzeAndFillMissingValues(unittest.TestCase):
    def test_fill_missing_values_numeric(self):
        df = pd.DataFrame(data_with_nan)

        expected_df = pd.DataFrame(expected_data_with_nan)

        result_df = analyze_and_fill_missing_values(df)
        pd.testing.assert_frame_equal(result_df, expected_df)


    def test_no_missing_values(self):
        df = pd.DataFrame(data_without_nan)

        expected_df = pd.DataFrame(expected_data_without_nan)

        result_df = analyze_and_fill_missing_values(df)
        pd.testing.assert_frame_equal(result_df, expected_df)


    def test_multiple_numeric_columns(self):
        df = pd.DataFrame(data_with_multiple_col_nan)

        expected_df = pd.DataFrame(expected_data_with_multiple_col_nan)

        result_df = analyze_and_fill_missing_values(df)
        pd.testing.assert_frame_equal(result_df, expected_df)


    def test_no_numeric_columns(self):
        df = pd.DataFrame(data_with_no_numerical)

        result_df = analyze_and_fill_missing_values(df)
        pd.testing.assert_frame_equal(result_df, df)

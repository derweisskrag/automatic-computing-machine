import unittest
from tomodachi_core.config_development.config import TEST_PATH
from tomodachi_core.tomodachi.services import PandasService, DatetimeService
from tomodachi_core.tomodachi.tests.testdata import PATH_TO_DATETIME_LIB

class TestDateChange(unittest.TestCase):
    def setUp(self):
        self.pandas_service = PandasService(TEST_PATH + PATH_TO_DATETIME_LIB)
        
        
    def test_data_change(self):
        with self.pandas_service.use_cached_data() as df:
             # check it is not zero        
             self.assertGreater(len(df), 0)


             # instantiate our datetime service
             datetime_service = DatetimeService(df)

             # let us use the method
             normalized_df = datetime_service.normalize_timestamps("Timestamp")

             # we can check several things
             # these guys are both object, right? 
             self.assertEqual(df["Timestamp"].dtype, "object")
             self.assertEqual(normalized_df["Timestamp"].dtype, "object")

             # Check if valid timestamps (yes they are)
             # this functions expects "str", rather Timestamp which is after that
             response = datetime_service.is_valid_timestamp("Timestamp")
             self.assertEqual(response, True)

             # However, when, we parse: there are no longer object, and instead we got datetime
             df["Timestamp"] = df["Timestamp"].astype(dtype="datetime64[ns]")
             self.assertEqual(df["Timestamp"].dtype, "datetime64[ns]")

             # and we can also check
             self.assertIsNone(df["Timestamp"].dt.tz, "It is None")


    def test_conversion_to_timestamp(self):
        with self.pandas_service.use_cached_data() as df:
            # it opened the csv data
            # let us change it timestamp
            # as the current type is "object"
            copied_df = df.copy() 
            service = DatetimeService(copied_df)
            copied_df = service.change_to_timestamp() # we look for the column "Timestamp" by default

            # let us test
            self.assertEqual(df["Timestamp"].dtype, "object")
            self.assertEqual(copied_df["Timestamp"].dtype, "datetime64[ns]", msg="The type of the copied_df is datetime64[ns]")
        

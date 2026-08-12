import unittest
from tomodachi_core.tomodachi.services.pandas_service import PandasService
from tomodachi_core.config_development.config import TEST_PATH

class HasDuplicatesTest(unittest.TestCase):
    def setUp(self):
        self.service = PandasService(TEST_PATH + "test_file.csv") # TEST_PATH / "test_file.csv"

    def test_duplicates(self):
        """
        In order to trigger duplicates, we have to understand what it means.
        It turns out that in Pandas, if a row has unique id, it will be unique. 
        
        """


        # read the file
        self.service.load_csv_data()

        # determine if we got duplicates
        self.assertTrue(self.service.has_duplicates(subset=["name", "wind_speed", "power_output"]))

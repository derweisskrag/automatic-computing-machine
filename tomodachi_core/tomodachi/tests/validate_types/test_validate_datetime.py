import unittest
from tomodachi_core.tomodachi.services import PandasService, DatetimeService
from tomodachi_core.tomodachi.tests.testdata.datetime_data.rules import rules

# We test this function:
from tomodachi_core.tomodachi.utils.check_data import validate

class TestValidateDatetime(unittest.TestCase):
    def setUp(self):
        self.service = PandasService("tomodachi_core/tomodachi/tests/testdata/datetime_data/lib.csv")
    

    def test_validate_data_wrong_format(self):
        # should be false
        with self.service.connection() as df:
            self.assertTrue(validate(df, rules_map=rules)) # Now it is True because Service fixed data automatically

    def test_validate_data_true_format(self):
        # should be true
        with self.service.connection() as df:
            # initialize the datetime service
            datetime_handler = DatetimeService(df)

            # apply dates to parse
            df = datetime_handler.fix_dates_format()

            # use pandas to parse 'object' to 'datetime64[ns]'
            df = datetime_handler.change_to_timestamp()

            # test: should be True
            self.assertTrue(validate(df, rules_map=rules))
            
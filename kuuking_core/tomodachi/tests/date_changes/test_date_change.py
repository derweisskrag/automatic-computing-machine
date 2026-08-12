import unittest
import pandas as pd
from tomodachi_core.config_development.config import TEST_PATH
from tomodachi_core.tomodachi.services.pandas_service import PandasService
from tomodachi_core.tomodachi.utils.tools import check_timestamp, validate_and_fix_timestamps

class TestDate(unittest.TestCase):
    def setUp(self):
        self.service = PandasService(TEST_PATH + "datetime_data/wrong_data.csv")
        

    def test_check_valid_data_return_bool(self):
        # read the file
        self.service.load_csv_data()

        # grabs the data frame
        df = self.service.df
        
        # now he calls
        isDateValid, errors = check_timestamp(df)

        """
            The function he called returns boolean type:
                - false
                - true
                (old version)

                - tuple[bool, int]:
                    - bool: the result of conversion,
                    - errors (int): the number of errors (for True -> we can only return True, as 0 isnt right)

            based on if pandas could parse the data, given the format ('%Y-%m-%d %H:%M:%S').

            This is function is simila to ours. Let us also pay attention that his functions 
            taken on 
                - df (pd.DataFrame)
                - column (str), whose default value is 'Timestamp' - the default value

            What do we expect from his function? True because if it parses -> it successful. 
            In Pandas, DataFrame is typed to "object", and hence it ain't the format. Right? However, we also
            remember that 

            >>> df["Timestamp"] = pd.to_datetime(df["Timestamp"])

            also worked. It could actually parse the "object" to "datetime64[ns]", and we had all
            dates valid. We also remember that 

            >>> df["Timestamp"] = df["Timestamp].astype(dtype="datetime64[ns]")

            worked, and it successfully parsed our "object" into Pandas 'Timestamp' type.

            NB! The 'object' and "2020-01-01" format belongs to Python's, not Pandas. So, what kind of 
            datetime we work with? -> Important
        """

        # Not null
        self.assertTrue(len(df) != 0) 

        # NOTICE: PandasService fixes the data automatically!
        # It has errors?
        # What was wrong before: returned int but expected bool, and then did not specify error (ValueError)
        self.assertTrue(isDateValid) # returns False because I added some problem to the file However
        self.assertEqual(errors, 0, "Exactly two errors") # oh, we got 0 errors

        # let us check Pandas types too
        self.assertNotEqual(df["Timestamp"].dtype, "object") # actually converted (<M8[ns])

        # we can now convert it to dateimte
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        self.assertEqual(df["Timestamp"].dtype, "datetime64[ns]")


    def test_try_fix_dates_return_valid_dates(self):
        # read the file
        self.service.load_csv_data()

        # get the df
        df = self.service.df

        # tries to apply his function
        fixed_df = validate_and_fix_timestamps(df)

        # Tries to verify if his lengths of DataFrames are eqaul
        # shouldBe -> True
        # Equal
        self.assertEqual(len(df),len(fixed_df)) # Yes, true

        # get the type of the fixed on
        self.assertEqual(fixed_df["Timestamp"].dtype, "object", "This is object right now")
        self.assertNotEqual(fixed_df["Timestamp"].dtype, "datetime64[ns]", "This not any 'datetime64[ns]' either")
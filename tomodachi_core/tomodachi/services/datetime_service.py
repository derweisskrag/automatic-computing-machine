"""
This service is used for managing the data
"""

import pandas as pd
from tomodachi_core.tomodachi.utils.tools import check_timestamp_sergei, validate_and_fix_timestamps

class DatetimeService:
    def __init__(self, df: pd.DataFrame) -> None:
        assert df is not None, f"Pandas DataFrame should NOT be None"
        self.df = df

    def is_valid_timestamp(self, column: str):
        """
        Checks if the provided timestamp column has valid timestamps ('YYYY-MM-DD HH:MM:SS' format).
        """
        return self.df[column].apply(check_timestamp_sergei).all()
    
    def normalize_timestamps(self, column: str) -> pd.DataFrame:
        """
        Normalize the timestamps to the format 'YYYY-MM-DD HH:MM:SS'.
        """
        if not self.is_valid_timestamp(column):
            raise ValueError(f"Invalid timestamp format in column: {column}")
        
        self.df[column] = pd.to_datetime(self.df[column]).dt.strftime('%Y-%m-%d %H:%M:%S')
        return self.df
    
    def change_to_timestamp(self, column="Timestamp"):
        """
        Changes from "object" to "Timestamp" and hence "datetime64[ns]"
        """
        self.df[column] = pd.to_datetime(self.df[column])
        return self.df
    
    def fix_dates_format(self, column="Timestamp"):
        """
        Fixes the format of the data, so we can parse them
        later into the correct 'datetime64[ns]' format

        Author: Danylo
        """
        self.df = validate_and_fix_timestamps(self.df, column=column)
        return self.df
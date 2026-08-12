"""
This module contains the Pandas Service that is used to 
do all the datascience pre-processing tasks that include:

Assignment tasks:

1. Timestamp and data format normalization
   - Validate and convert all timestamp values to the format YYYY-MM-DD HH:MM:SS.
   - Correct any incorrectly formatted or missing timestamp values.

2. Analysis and filling of missing values
   - Analyze which columns contain missing data.
   - Determine appropriate strategies for filling in the missing values (e.g., mean, median, or relevant substitutions).

3. Duplicate detection and removal
   - Identify and remove duplicate entries based on a combination of timestamp and wind data.

4. Validation of categorical variables
   - Check and standardize category labels (e.g., unify “mm” and “Millimeter” in precipitation units).

5. Data structure validation and creation of the cleaned file
   - Ensure all columns meet expectations (e.g., numerical data should not contain text).
   - Save the cleaned dataset as cleaned_Synthetic_Wind_Power.csv.
"""

from functools import cached_property
from contextlib import contextmanager
from typing import Generator, override
from tomodachi_core.tomodachi.services.preprocess import PreprocessData
from tomodachi_core.common_types.result import Result, Ok, Err, result_wrapper
from tomodachi_core.common_types.option import Some, Option
from tomodachi_core.tomodachi.internals.service import Service
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class PandasService(Service):
    def __init__(self, path: str = "") -> None:
        super().__init__(path)
        self.preprocessor = PreprocessData()
        

    @override
    def load_csv_data(self):
        match super().load_csv_data():
            case Ok(value=df) if isinstance(df, pd.DataFrame):
                return df
            case Err(error=error):
                return Err(error=error)


    def has_duplicates(self, subset: list[str]) -> bool:
        """
            Checks if the data has duplicate values in the following columns:

            - Timestamps
            - Wind data: Wind_Speed, etc
            ["Timestamps", "Wind_Speed", "Wind_Dust", "Wind_Direction"]
        """
        return len(self.df[self.df.duplicated(subset=subset)]) != 0
    

    def remove_duplicates(self, subset: list[str]) -> Result[pd.DataFrame, str]:
        try:
            if self.has_duplicates(subset=subset):
                cleaned_df = self.df.drop_duplicates(subset=subset)
                return Ok(value=cleaned_df)
        except Exception as e:
            return Err(error=f"Error while removing duplicates: {e!s}")
        

    def preprocess_df(self, df: pd.DataFrame, strategy: Option[str], columns: Option[list[str]]) -> Option[pd.DataFrame]:
        if df is None:
            return None

        match self.preprocessor.preprocess_df(df, strategy, columns):
            case Ok(value=new_df) if isinstance(new_df, pd.DataFrame):
                return Some(new_df)
            case Err(error=e) if isinstance(e, Exception):
                logging.error(f"Preprocessing failed: {e}")
                return None


    def update_dataframe(self, new_df: pd.DataFrame) -> None:
        # If we want to keep the logger:
        ret = super().set_df(new_df)
        if ret.is_err():
            logging.error(f"Error while updating the DataFrame: {ret.unwrap_err()}")
            return ret # propage the error
        else:
            logging.info("DataFrame updated successfully.")

        return self
            

    def save_dataframe(self, path: str) -> None:
        # If we want to keep the logger:
        ret = super().save_to_path(path)
        if ret.is_err():
            logging.error(f"Error while saving the DataFrame: {ret.unwrap_err()}")
            return ret
        else:
            logging.info(f"DataFrame saved successfully to {path}.")
        return self

        
    @contextmanager
    def connection(self) -> Generator[pd.DataFrame, None, None]:
        """
        For temporary data manipulation
        """
        service = None
        try:
            service = PandasService(self.path)
            service.load_csv_data()
            yield service.get_df().unwrap()
        finally:
            if service:
                logging.info(f"Finished working with data from {self.path}")


    @contextmanager
    def use_cached_data(self) -> Generator[pd.DataFrame, None, None]:
        """
        For temporary data manipulation with cached data
        """
        service = None
        try:
            service = PandasService(self.path)
            df = service.cached_df
            yield df
        finally:
            if service:
                logging.info(f"Finished working with data from {self.path}")


    @cached_property
    @override
    def get_mock_dataframe(self) -> pd.DataFrame:
        df = super().get_mock_dataframe().unwrap_or(pd.DataFrame([{"country": "USA", "population": "100000000"}]))
        return df
    

    @staticmethod
    def from_dict(d: dict) -> Result[pd.DataFrame, str]:
        try:
            if not isinstance(d, dict):
                return Err(f"Expected a dictionary, but got {type(d).__name__}")

            return (
                Ok(pd.DataFrame(d))
                    .map(lambda x: x.dropna())
                    .and_then(
                        lambda df: Ok(df.assign(Timestamp=pd.to_datetime(df["Timestamp"]))) if "Timestamp" in df.columns else df)
            )
        except Exception as e:
            return Err(error=e)
        
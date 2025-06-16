"""
This service provides a base class for all services in the application.

It provides a set of internal functions that is used by PandasService and other services.
"""
from functools import cached_property
from tomodachi_core.common_types.result import Result, Ok, Err, result_wrapper
import pandas as pd


"""
TODO: Implement the necessary methods for data processing and manipulation.
Remove the path requirement from the constructor and fix all the tests that will fail due to path not being mandatory.

Our Service class is a base class for all services in the application.

PandasService will use the DataFrame or reading from files. 
To let users be able to use the service without providing a path, we will remove the path requirement from the constructor.
"""

class Service:
    def __init__(self, path: str) -> None:
        if not isinstance(path, str):
            raise ValueError("Please, provide valid path!")
        
        self.path = path


    def load_csv_data(self) -> Result[pd.DataFrame, str]:
        try:
            df = pd.read_csv(self.path)

            self.df = (
                Ok(df)
                .and_then(self.remove_unnamed_and_convert_dates)
                .and_then(self.remove_millimeters)
                .unwrap() 
            )

            return Ok(self.df)
        except (
            FileNotFoundError, 
            pd.errors.ParserError,
              pd.errors.EmptyDataError, 
              Exception
              ) as e:
            return Err(e)
        

    def remove_unnamed_and_convert_dates(self, df: pd.DataFrame) -> Result[pd.DataFrame, str]:
        try:
            if "Unnamed: 0" in df.columns:
                df = df.drop(columns=["Unnamed: 0"])
            if "Timestamp" in df:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], infer_datetime_format=True, errors='coerce')
            return Ok(df)
        except (KeyError, pd.errors.ParserError) as e:
            return Err(error=e)
        except Exception as e:
            return Err(str(e))


    def remove_millimeters(self, df: pd.DataFrame) -> Result[pd.DataFrame, str]:
        """
        Rename columns that contain 'millimeter' (case-insensitive) 
        to replace 'millimeter' with 'mm'.
        """
        try:
            if "Precipitation_Unit" in df.columns:
                df["Precipitation_Unit"] = df["Precipitation_Unit"].replace("milimeter", "mm")

                df["Precipitation_Unit"] = df["Precipitation_Unit"].str.lower()
                df["Precipitation_Unit"] = df["Precipitation_Unit"].replace(
                    to_replace=r"(m\s*|mi\s*|mil\s*|milli\s*)?l?lit(er|re)?s?",
                    value="mm",
                    regex=True
                )
                df["Precipitation_Unit"] = df["Precipitation_Unit"].str.strip()
            return Ok(df)
        except Exception as e:
            return Err(str(e))



    @cached_property
    def cached_df(self):
        return pd.read_csv(self.path)
    

    def get_df(self) -> pd.DataFrame:
        if hasattr(self, 'df') and self.df is not None:
            return Ok(self.df)
        else:
            return Err("DataFrame is not loaded or does not exist.")
        

    def set_df(self, df: pd.DataFrame) -> Result[pd.DataFrame, str]:
        if isinstance(df, pd.DataFrame):
            self.df = df
            return Ok(df)
        else:
            return Err("Provided object is not a valid DataFrame.")
        

    def get_clean_df(self) -> Result[pd.DataFrame, str]:
        if not hasattr(self, 'df') or self.df is None:
            return Err("DataFrame not loaded.")
        return (
            Ok(self.df)
            .and_then(self.remove_unnamed_and_convert_dates)
            .and_then(self.remove_millimeters)
        )
        

    def save_to_path(self, path: str) -> Result[str, str]:
        if path is None:
            return Err("The path cannot be None")
        try:
            self.df.to_csv(path, index=False)
            return Ok(path)
        except Exception as e:
            return Err(f"Error while saving the DataFrame: {e}")
        
    
    def get_mock_dataframe(self) -> Result[pd.DataFrame, str]:
        """
        This methods returns the mock data to get sample for 
        working with pandas library.

        Returns:
            Ok(pd.DataFrame) -> if no error
            Err(str) -> if something goes wrong
        """
        employees: dict = [
            {
                "name": "Alice",
                "age": 21,
                "profession": "teacher",
                "salary": "4700 USD",
                "hobby": "garden",
                "country": "USA",
                "phone": "iPhone"
            },
            {
                "name": "Joe",
                "age": 38,
                "profession": "taxi driver",
                "salary": "2100 EU",
                "hobby": "chess",
                "country": "France",
                "phone": "android"
            },
            {
                "name": "Vasily",
                "age": 42,
                "profession": "civil engineer",
                "salary": "420,000 RUB",
                "hobby": "gaming",
                "country": "Russia",
                "phone": "android"
            },
            {
                "name": "Michele",
                "age": 19,
                "profession": "chef assistant",
                "salary": "1200 EUR",
                "hobby": "fishing",
                "country": "Italy",
                "phone": "iPhone"
            },
            {
                "name": "Sakura",
                "age": 27,
                "profession": "web developer",
                "salary": "350,000 JPY",
                "hobby": "drawing",
                "country": "Japan",
                "phone": "android"
            }
        ]

        return Ok(pd.DataFrame(employees))
    

    @staticmethod
    def is_dataframe(df: pd.DataFrame) -> Result[bool, str]:
        if isinstance(df, pd.DataFrame):
            return Ok(True)
        return Err(f"Expected DataFrame, but got {type(df).__name__}")


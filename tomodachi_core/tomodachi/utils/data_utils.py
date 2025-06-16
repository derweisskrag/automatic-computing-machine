"""
This module contains the functionality related to process data for the NaN 
presence and then Handles the NaN functionality. 

Available functions:
    - contains_nan(df: pd.DataFrame, columns: Union[List[str], str] = []) -> bool
        This functions checks if the given DataFrame in the specific column(s) contain
        the NaN values. 

    - select_columns_with_nan(df: pd.DataFrame) -> Result[List[], str]
        Selects those columns that contain NaN values

    - analyze_and_fill_missing_values(df: pd.DataFrame) -> pd.DataFrame 
        gets the DataFrame to process NaN values using the functions above

    - fill_nan_with_median(df: pd.DataFrame, column: str) -> pd.DataFrame
        This functions fills the data frame column missing data with median 

    For more information, please refer to tests/handle_nan
"""


import pandas as pd
from typing import Union, List
from tomodachi_core.common_types.result import Result


def contains_nan(df: pd.DataFrame, columns: Union[List[str], str, None] = None) -> bool:
    return df.isna().sum() > 0 if columns is None else df[columns].isna().sum() > 0

def select_columns_with_nan(df: pd.DataFrame) -> Result[List[int], str]:
    if len(df) == 0:
        return Result(error=f"No NaN were processed by the function, as the Pandas DataFrame is empty:\n{df.head()}")
    elif not isinstance(df, pd.DataFrame):
        return Result(error=f"The provided data was not the Pandas DataFrame type: {df}")

    # try computing
    ret = [col for col in df.select_dtypes(include="number").columns if contains_nan(df, col)]

    if len(ret) == 0:
        # Special case
        # print("Could not process the DataFrame: all columns do NOT contain NaN")
        return Result(value=ret)

    return Result(value=ret)


def fill_nan_with_median(df: pd.DataFrame, column: str) -> pd.DataFrame:
    # compute the median
    median_value = df[column].median()

    # update the data frame
    df[column] = df[column].fillna(median_value)
    return df


def analyze_and_fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    This functions analyzes the DataFrame data and finds the 
    empty values and fills the missing value as median. So,
    processed DataFrame would actually contain 0 NaN.

    Args:
        df (pd.DataFrame) - a Pandas DataFrame object that holds
            the data
        
    Returns
        result (pd.DataFrame) - a modified the Pandas DataFrame
    """

    response = select_columns_with_nan(df)

    match response.is_ok():
        case True:
            # process the NaN
            # grab columns
            columns = response.unwrap()

            if len(columns) == 0:
                # just return, no modification
                return df
            else:
                # process and fill the median
                for col in columns:
                    fill_nan_with_median(df, col)
        case False:
            # we got an error
            # This will raise the error
            response.unwrap()
        case _:
            print("Unexpected error! Attempting to exit")
            exit()

    return df
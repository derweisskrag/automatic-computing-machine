"""
This module contains the utility functions

"""

import pandas as pd
from typing import Dict, Iterable, Generator, Union
from dateutil.parser import parse

from tomodachi_core.common_types.test_people import TestPeople
from tomodachi_core.tomodachi.utils import DATE_FORMATS

def check_timestamp_sergei(ts: str) -> bool:
    try:
        parse(ts)
        return True
    except ValueError:
        return False

# this is Danil function
def check_timestamp(df: pd.DataFrame, column: str = 'Timestamp') -> tuple[bool, int]: # you wanna return what?
    """Исправляет формат даты в DataFrame."""
    try:
        df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S')
        return True, 0
    except ValueError:
        df[column] = pd.to_datetime(df[column], errors='coerce')
        errors = df[column].isna().sum()
        return False, errors
    

# TODO: Format it properly -> do it later 
def validate_and_fix_timestamps(df: pd.DataFrame, column: str ='Timestamp', correct_format: str ='%Y-%m-%d %H:%M:%S'):
    # maybe dateutil.parse.parse???
    def try_parse_date(date_str):
        if pd.isna(date_str):
            return pd.NaT
        
        for fmt in DATE_FORMATS:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT
    
    # so, what happens here?
    # this will make them to datetime (<MC8[ns] == datetime64[ns]) - Yup!
    df[column] = df[column].apply(try_parse_date)

    # this one is similar to mine -> hence object - yup!
    df[column] = df[column].dt.strftime(correct_format) # you may not need this!
    return df

def process_dictionary_data(data: TestPeople) -> str:
    """
    Author: Sergei
    """
    
    try:
        # Check if the data is valid for CSV conversion
        if not can_to_csv(data):
            raise ValueError("The provided dictionary data cannot be converted to CSV format!")

        # If validation passed, proceed with the transformation to CSV
        result = ",".join(data.keys()) + "\n"
        
        # Iterate over the data values and create rows
        for item in traverse(*data.values()):
            result += ",".join(map(str, item)) + "\n"
                
        return result
    except (TypeError, ValueError) as e:
        # Catch the specific exception and re-raise it with extra context
        raise Exception(f"Error while processing data for CSV conversion: {e}")


def traverse(*lsts: Iterable[Union[int, str]]) -> Generator[tuple[Union[int, str], ...], None, None]:
    """
    Traverses multiple iterables in parallel and yields tuples of values.
    """
    for tuple_values in zip(*lsts):
        yield tuple_values


def can_to_csv(data: Dict[str, Iterable[Union[int, str]]]) -> bool:
    """
    It only processes my case:
        all keys are strings but values are strings
    
    """
    if not isinstance(data, dict): 
        raise TypeError("Please, provide the correct dictionary!")
    
    for key, value in data.items():
        if not isinstance(value, Iterable):
            raise TypeError(f"The value for key '{key}' is not an iterable! Found type: {type(value)}")

        if len(value) == 0:  # Check if any list is empty
            raise ValueError(f"The list for key '{key}' is empty!")

    # Ensure all lists have the same length
    lengths = [len(value) for value in data.values()]
    if len(set(lengths)) > 1:  # If the lengths are not all the same
        raise ValueError("All lists must have the same length!")
    
    return True
    



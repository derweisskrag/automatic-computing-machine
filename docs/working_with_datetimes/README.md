# Working with Dates in Python and Pandas

## Table of Contents

1. [Introduction](#introduction)
2. [Python's `datetime` module](#pythons-datetime-module)
3. [Pandas `datetime` Module](#pandas-datetime-module)
4. [Pandas vs Python `datetime` Type](#pandas-vs-python-datetime-type)
    - [Why Convert to Python `datetime`?](#why-convert-to-python-datetime)
    - [Conversion Steps](#conversion-steps)
5. [Functions](#functions)
    - [`check_timestamp_sergei`](#check_timestamp_sergei)
    - [`check_timestamp`](#check_timestamp)
    - [`validate_and_fix_timestamps`](#validate_and_fix_timestamps)
6. [Conclusion](#conclusion)

## Introduction

Working with dates and times is essential in many data analysis tasks. Both Python's standard library and Pandas provide powerful tools for handling date and time data. This document outlines the common datetime types and functions from both Python and Pandas, as well as their interaction.

### Python's `datetime` module

The `datetime` module in Python provides several classes for working with dates and times. Two of the most commonly used classes are:

- `datetime.date`: Represents a date (year, month, day) without time.
    Example:
    ```python
    import datetime
    today = datetime.date.today()
    print(today)  # Output: 2025-04-21
    ```
- `datetime.datetime`: Represents both a date and time.
    Example:
    ```python
    import datetime
    now = datetime.datetime.now()
    print(now)  # Output: 2025-04-21 14:52:35.843702
    ```

Both of these classes are part of the `datetime` module, and they can be used for parsing and manipulating date/time objects. However, when working with tabular data in Pandas, these types often need to be converted to a compatible format for efficient processing.

### Pandas `datetime` Module

Pandas provides its own datetime handling capabilities which are often more efficient when dealing with large datasets. The primary difference between Python's `datetime` and Pandas' datetime is that Pandas uses `datetime64[ns]` (Nanosecond precision) internally, which is optimized for performance with time series data.

- `pd.to_datetime()`: This function is used to convert strings or other datetime-like objects into Pandas' datetime type.
    Example:
    ```python
    import pandas as pd
    df = pd.DataFrame({'date': ['2025-04-21 14:52:35', '2025-04-22 15:12:25']})
    df['date'] = pd.to_datetime(df['date'])
    print(df)
    ```

- Pandas `datetime64[ns]`: This is the data type used by Pandas for storing datetime values. It is more efficient than Python’s `datetime.datetime` for large datasets and supports vectorized operations.

### Pandas vs Python `datetime` Type

Pandas `datetime64[ns]` is a more efficient and optimized type for working with large datasets, especially in dataframes. However, sometimes we need to convert between Python's `datetime` objects and Pandas' `datetime64[ns]` for compatibility and to avoid issues with invalid formats.

#### Why Convert to Python `datetime`?

When dealing with mixed data formats or unknown inputs, it’s important to first parse the datetime string into a Python `datetime` object (using Python’s `datetime` or `dateutil.parser`) before converting it to Pandas’ `datetime64[ns]` type. This ensures that any invalid formats are handled properly before you try to manipulate them in Pandas.

##### Conversion Steps:

1. Parse the date using `dateutil.parser` or Python’s `datetime`.

2. Convert it to Pandas `datetime64[ns]` using `pd.to_datetime()`.

This two-step process is crucial to ensure data integrity and avoid errors during conversion.

### Functions

#### `check_timestamp_sergei`

This function checks if a given timestamp string is valid by attempting to parse it using the `dateutil.parser.parse` function.

```python
def check_timestamp_sergei(ts: str) -> bool:
    try:
        parse(ts)
        return True
    except ValueError:
        return False

print(check_timestamp_sergei("2025-05-01")) # true
print(check_timestamp_sergei("2025-x-05")) # False
```

##### Parameters:

`ts`: A string representing a timestamp.

##### Returns:

`True` if the timestamp can be parsed successfully.

`False` if the timestamp is invalid.


#### `check_timestamp`

This function checks and fixes the format of a timestamp column in a Pandas DataFrame. It first tries to convert the column to the specified format. If it encounters errors, it coerces invalid entries to `NaT` (Not a Time) and counts how many errors there are.

```python
def check_timestamp(df: pd.DataFrame, column: str = 'Timestamp') -> tuple[bool, int]:
    try:
        df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S')
        return True, 0
    except ValueError:
        df[column] = pd.to_datetime(df[column], errors='coerce')
        errors = df[column].isna().sum()
        return False, errors

is_valid, _ = pd.DataFrame({"Timestamp": ["2025-01-05 16:00:00", "2025-03-07 00:00:00"], "values": [10, 20]})
print(is_valid) # true
```

##### Parameters:

1. `df`: A Pandas DataFrame containing a column of timestamp strings.

2. `column`: The name of the column containing timestamps (default is 'Timestamp').

##### Returns

A tuple with:

--`True` if the column is successfully converted to datetime, `False` if there are errors.

- The count of invalid entries (`NaT`).

#### `validate_and_fix_timestamps`

This function attempts to parse and fix timestamps in a given DataFrame column. It handles multiple formats by trying different predefined formats and converts valid entries into a standard format.

```python
def validate_and_fix_timestamps(df: pd.DataFrame, column: str ='Timestamp', correct_format: str ='%Y-%m-%d %H:%M:%S'):
    def try_parse_date(date_str):
        if pd.isna(date_str):
            return pd.NaT
        
        for fmt in DATE_FORMATS:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT
    
    df[column] = df[column].apply(try_parse_date)
    df[column] = df[column].dt.strftime(correct_format)
    return df
```

##### Parameters:

- `df`: A Pandas DataFrame containing a column with timestamp strings.

- `column`: The name of the column containing timestamps (default is 'Timestamp').

- `correct_format`: The format string to which all valid timestamps should be converted (default is '%Y-%m-%d %H:%M:%S').

##### Returns:

The `DataFrame` with the timestamp column corrected.

### Conclusion

Working with date and time in Python and Pandas is a crucial part of data analysis. Understanding the differences between Python's `datetime` and Pandas' `datetime64[ns]` type, and knowing when and how to convert between them, ensures data integrity and smooth processing.

By using these helper functions, you can easily check, validate, and correct timestamp columns in your DataFrame, making it much easier to handle datetime data in your workflows.
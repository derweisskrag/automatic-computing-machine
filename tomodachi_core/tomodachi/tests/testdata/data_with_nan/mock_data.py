from numpy import nan

data_with_nan = {
    'A': [1, 2, nan, 4],
    'B': [nan, 2, 3, 4],
    'C': ['a', 'b', 'c', 'd'],
}

data_with_multiple_col_nan = {
    'A': [1, nan, 3, 4],
    'B': [nan, nan, 7, 8],
    'C': [10, 20, 30, 40]
}

expected_data_with_nan = {
    'A': [1, 2, 2.0, 4],
    'B': [3.0, 2, 3, 4],
    'C': ['a', 'b', 'c', 'd'],
}

expected_data_with_multiple_col_nan = {
    'A': [1, 3.0, 3, 4],
    'B': [7.5, 7.5, 7, 8],
    'C': [10, 20, 30, 40]
}


data_without_nan = {
    'A': [1, 2, 3, 4],
    'B': [1, 2, 3, 4],
    'C': ['a', 'b', 'c', 'd'],
}

expected_data_without_nan = {
    'A': [1, 2, 3, 4],
    'B': [1, 2, 3, 4],
    'C': ['a', 'b', 'c', 'd'],
}


data_with_no_numerical = {
    'A': ['a', 'b', nan, 'd'],
    'B': ['e', 'f', 'g', 'h'],
}

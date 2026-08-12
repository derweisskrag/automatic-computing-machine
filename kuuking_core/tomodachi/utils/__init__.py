from tomodachi_core.tomodachi.utils.data_utils import analyze_and_fill_missing_values

# used for testing
# we can remove -> Negotiate
SUBSETS = {
    "subsets": ["Timestamp", "Wind_Speed", "Wind_Gust", "Wind_Direction"]
}

DATE_FORMATS: str = [
        '%Y-%m-%d %H:%M:%S',   
        '%d-%m-%Y %H:%M:%S',  
        '%B %d, %Y %H:%M:%S',  
        '%m-%d-%Y %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',   
        '%Y/%m/%d %H:%M:%S',   
        '%d/%m/%Y %H:%M:%S',     
        '%Y.%m.%d %H:%M:%S',     
    ]


# Pandas Types
expected_types = {
        "Timestamp": "datetime64[ns]",
        "Wind_Speed": "float64",
        "Wind_Gust": "float64",
        "Wind_Direction": "int64",
        "Temperature": "float64",
        "Humidity": "float64",
        "Precipitation": "float64",
        "Pressure": "float64",
        "Cloud_Cover": "float64",
        "Solar_Radiation": "float64",
        "Hour_of_Day": "int64",
        "Day_of_Week": "int64",
        "Month": "int64",
        "Wind_Speed_Squared": "float64",
        "Wind_Speed_Cubed": "float64",
        "Power_Output": "float64",
        "Precipitation_Unit": "object",
    }
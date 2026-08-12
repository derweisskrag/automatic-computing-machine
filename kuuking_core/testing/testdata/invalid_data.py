"""
Here I dump the invalid data I used to test the validation functions.

What is included:
- Wrong data types (e.g. string instead of int)
- invalid datetimes 
"""

invalid_timestamps_wrong_timezone = [
    "2023-10-01T00:00:00Z",      # Correct ISO format but wrong timezone (UTC instead of expected one)
    "2023-10-01T00:00:00+00:00", # Correct ISO with offset but still wrong timezone
    "2023-10-01T00:00:00+01:00", # Correct ISO with +1 hour offset but wrong timezone
    "2023-10-01T00:00:00-05:00", # Another wrong timezone (UTC-5)
    "2023-10-01T12:00:00+09:00", # Tokyo timezone, wrong if expecting UTC or specific timezone
    "2023-10-01T00:00:00+03:00", # Moscow time, wrong timezone
    "2023-10-01T23:59:59-08:00", # PST time, wrong timezone
]

invalid_timestamps = [
    # no timezones
    "2023-05-06",                 # Date only, no time or timezone
    "2024/01/15 12:30:00",         # Slashes instead of dashes
    "12-25-2023",                  # U.S. format MM-DD-YYYY
    "2023.08.20",                  # Dots instead of dashes
    "2023-11-03 10:00",            # Missing seconds and timezone
    "2025-02-30",                  # Invalid date (Feb 30 does not exist)
    "2024-04-31",                  # April has only 30 days
    "2023-02-28T25:61:00",         # Invalid time (hours > 24, minutes > 60)

    # wrong formats
    "2023-07-01T00:00",            # Missing seconds and timezone
    "2023-09-18 23:59:59.12345",   # Too many milliseconds without 'Z' or timezone
    "20231201T080000Z",            # Compact ISO format without separators
    "01-01-2025 14:00:00 UTC",     # Incorrectly formatted with space and UTC label
    "2026 year, second of January",# Natural language, not a timestamp
    "March 5, 2024 08:00",         # Written English date
    "15/04/2025 13:00",            # European format with slashes
    "2023-13-01T00:00:00",         # 13th month doesn't exist
    "2023-00-10T00:00:00",         # 0th month doesn't exist
    "2023-01-00T00:00:00",         # 0th day doesn't exist
    "2023-11-03T24:01:00",         # Invalid hour (24:01)
]



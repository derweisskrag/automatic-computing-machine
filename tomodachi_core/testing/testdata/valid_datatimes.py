"""
Here are some valid data examples I used to test the validation functions.

"""
valid_timestamps_no_timezone = [
    "2023-10-01T00:00:00",   # Correct ISO format (without timezone)
    "2023-12-25T12:00:00",   # Christmas time (no timezone)
    "2024-02-29T23:59:59",   # Leap year (no timezone)
    "2025-01-01T00:00:00",   # New Year's midnight (no timezone)
    "2023-06-15T14:30:00",   # Afternoon (no timezone)
    "2023-09-10T09:45:00",   # Morning (no timezone)
    "2024-11-03T01:30:00",   # DST transition day (no timezone)
    "2023-05-20T00:00:00",   # Midnight (no timezone)
    "2023-08-01T12:00:00",   # Noon (no timezone)
    "2023-07-15T10:30:00",   # Morning (no timezone)
]


valid_timestamps = [
    "2023-10-01T00:00:00+02:00",  # Correct format with specific timezone (UTC+2, e.g., Central European Time)
    "2023-12-25T12:00:00Z",       # Christmas, UTC timezone
    "2024-02-29T23:59:59Z",       # Leap year, Feb 29 exists in 2024
    "2025-01-01T00:00:00+00:00",  # New Year's midnight UTC
    "2023-06-15T14:30:00+01:00",  # Valid timestamp with +01:00 offset
    "2023-09-10T09:45:00-04:00",  # Valid timestamp, UTC-4 (Eastern Time in summer)
    "2024-11-03T01:30:00-07:00",  # DST transition day in US (fall back)
    "2023-03-12T02:30:00-08:00",  # DST spring forward time (even if 02:30 may not exist, parsers handle)
    "2023-05-20T00:00:00+05:30",  # Indian Standard Time (UTC+5:30)
    "2023-08-01T12:00:00+10:00",  # Australian Eastern Standard Time (AEST)
]


valid_timestamps_no_timezone_with_date_only = [
    "2023-10-01",             # Date only, valid
    "2024-02-29",             # Date only, leap year date
    "2025-01-01",             # Date only, New Year's Day
    "2023-06-15",             # Date only
    "2023-09-10",             # Date only
    "2024-11-03",             # Date only
    "2023-05-20",             # Date only
    "2023-08-01",             # Date only
    "2023-07-15",             # Date only
    "2023-03-05",             # Date only
]

valid_dates_no_timezone = [
    "2023-10-01",             # ISO 8601 format (YYYY-MM-DD)
    "2024/02/29",             # Slash-separated date (YYYY/MM/DD)
    "2025-01-01",             # ISO 8601 format (YYYY-MM-DD)
    "12-25-2023",             # U.S. format (MM-DD-YYYY)
    "2023.12.25",             # Dot-separated date (YYYY.MM.DD)
    "2023-07-04",             # ISO 8601 format (YYYY-MM-DD)
    "01/15/2024",             # U.S. format (MM/DD/YYYY)
    "2024.03.05",             # Dot-separated date (YYYY.MM.DD)
    "2023-11-03",             # ISO 8601 format (YYYY-MM-DD)
    "2023-08-22",             # ISO 8601 format (YYYY-MM-DD)
    "23/05/2023",             # European format (DD/MM/YYYY)
    "2023-06-15",             # ISO 8601 format (YYYY-MM-DD)
    "2023/04/25",             # Slash-separated date (YYYY/MM/DD)
    "15-07-2023",             # European format (DD-MM-YYYY)
    "2023.09.30",             # Dot-separated date (YYYY.MM.DD)
    "2023-01-01",             # ISO 8601 format (YYYY-MM-DD)
    "2025/05/21",             # Slash-separated date (YYYY/MM/DD)
    "07-10-2023",             # U.S. format (MM-DD-YYYY)
]


# valid dates but "/" format
valid_dates_slash_format = [
    "2023/10/01",             # Slash-separated date (YYYY/MM/DD)
    "2024/02/29",             # Slash-separated date (YYYY/MM/DD)
    "2025/01/01",             # Slash-separated date (YYYY/MM/DD)
    "12/25/2023",             # U.S. format (MM/DD/YYYY)
    "2023/07/04",             # Slash-separated date (YYYY/MM/DD)
    "01/15/2024",             # U.S. format (MM/DD/YYYY)
    "2024/03/05",             # Slash-separated date (YYYY/MM/DD)
    "2023/11/03",             # Slash-separated date (YYYY/MM/DD)
    "2023/08/22",             # Slash-separated date (YYYY/MM/DD)
    "23/05/2023",             # European format (DD/MM/YYYY)
    "2023/06/15",             # Slash-separated date (YYYY/MM/DD)
    "2023/04/25",             # Slash-separated date (YYYY/MM/DD)
    "15/07/2023",             # European format (DD/MM/YYYY)
    "2023/09/30",             # Slash-separated date (YYYY/MM/DD)
    "2023/01/01",             # Slash-separated date (YYYY/MM/DD)
    "2025/05/21",             # Slash-separated date (YYYY/MM/DD)
]

valid_dates_dot_format = [
    "2023.10.01",             # Dot-separated date (YYYY.MM.DD)
    "2024.02.29",             # Dot-separated date (YYYY.MM.DD)
    "2025.01.01",             # Dot-separated date (YYYY.MM.DD)
    "12.25.2023",             # U.S. format (MM.DD.YYYY)
    "2023.07.04",             # Dot-separated date (YYYY.MM.DD)
    "01.15.2024",             # U.S. format (MM.DD.YYYY)
    "2024.03.05",             # Dot-separated date (YYYY.MM.DD)
    "2023.11.03",             # Dot-separated date (YYYY.MM.DD)
    "2023.08.22",             # Dot-separated date (YYYY.MM.DD)
    "23.05.2023",             # European format (DD.MM.YYYY)
    "2023.06.15",             # Dot-separated date (YYYY.MM.DD)
    "2023.04.25",             # Dot-separated date (YYYY.MM.DD)
    "15.07.2023",             # European format (DD.MM.YYYY)
    "2023.09.30",             # Dot-separated date (YYYY.MM.DD)
    "2023.01.01",             # Dot-separated date (YYYY.MM.DD)
    "2025.05.21",             # Dot-separated date (YYYY.MM.DD)
]

valid_dates_iso_format = [
    "2023-10-01",             # ISO 8601 format (YYYY-MM-DD)
    "2024-02-29",             # Leap year date (YYYY-MM-DD)
    "2025-01-01",             # New Year's Day (YYYY-MM-DD)
    "2023-07-04",             # Independence Day (YYYY-MM-DD)
    "2023-05-20",             # Random date (YYYY-MM-DD)
    "2023-11-03",             # Random date (YYYY-MM-DD)
    "2023-06-15",             # Random date (YYYY-MM-DD)
    "2023-08-22",             # Random date (YYYY-MM-DD)
    "2023-12-31",             # Year-end date (YYYY-MM-DD)
    "2024-03-25",             # Random date (YYYY-MM-DD)
    "2025-02-15",             # Random date (YYYY-MM-DD)
    "2023-09-15",             # Random date (YYYY-MM-DD)
    "2024-04-10",             # Random date (YYYY-MM-DD)
    "2023-02-28",             # Non-leap year date (YYYY-MM-DD)
    "2023-01-01",             # New Year's Day (YYYY-MM-DD)
    "2025-05-21",             # Random date (YYYY-MM-DD)
]

valid_dates_european_format = [
    "01-10-2023",             # European format (DD-MM-YYYY)
    "29-02-2024",             # Leap year date (DD-MM-YYYY)
    "01-01-2025",             # New Year's Day (DD-MM-YYYY)
    "04-07-2023",             # Independence Day (DD-MM-YYYY)
    "20-05-2023",             # Random date (DD-MM-YYYY)
    "03-11-2023",             # Random date (DD-MM-YYYY)
    "15-06-2023",             # Random date (DD-MM-YYYY)
    "22-08-2023",             # Random date (DD-MM-YYYY)
    "31-12-2023",             # Year-end date (DD-MM-YYYY)
    "25-03-2024",             # Random date (DD-MM-YYYY)
    "15-02-2025",             # Random date (DD-MM-YYYY)
    "15-09-2023",             # Random date (DD-MM-YYYY)
    "10-04-2024",             # Random date (DD-MM-YYYY)
    "28-02-2023",             # Non-leap year date (DD-MM-YYYY)
    "01-01-2023",             # New Year's Day (DD-MM-YYYY)
    "21-05-2025",             # Random date (DD-MM-YYYY)
]

valid_dates_slash_consistent = [
    "2023/10/01",             # Slash-separated date (YYYY/MM/DD)
    "2024/02/29",             # Leap year date (YYYY/MM/DD)
    "2025/01/01",             # New Year's Day (YYYY/MM/DD)
    "2023/07/04",             # Independence Day (YYYY/MM/DD)
    "2023/05/20",             # Random date (YYYY/MM/DD)
    "2023/11/03",             # Random date (YYYY/MM/DD)
    "2023/06/15",             # Random date (YYYY/MM/DD)
    "2023/08/22",             # Random date (YYYY/MM/DD)
    "2023/12/31",             # Year-end date (YYYY/MM/DD)
    "2024/03/25",             # Random date (YYYY/MM/DD)
    "2025/02/15",             # Random date (YYYY/MM/DD)
    "2023/09/15",             # Random date (YYYY/MM/DD)
    "2024/04/10",             # Random date (YYYY/MM/DD)
    "2023/02/28",             # Non-leap year date (YYYY/MM/DD)
    "2023/01/01",             # New Year's Day (YYYY/MM/DD)
    "2025/05/21",             # Random date (YYYY/MM/DD)
]


valid_dates_dot_consistent = [
    "2023.10.01",             # Dot-separated date (YYYY.MM.DD)
    "2024.02.29",             # Leap year date (YYYY.MM.DD)
    "2025.01.01",             # New Year's Day (YYYY.MM.DD)
    "2023.07.04",             # Independence Day (YYYY.MM.DD)
    "2023.05.20",             # Random date (YYYY.MM.DD)
    "2023.11.03",             # Random date (YYYY.MM.DD)
    "2023.06.15",             # Random date (YYYY.MM.DD)
    "2023.08.22",             # Random date (YYYY.MM.DD)
    "2023.12.31",             # Year-end date (YYYY.MM.DD)
    "2024.03.25",             # Random date (YYYY.MM.DD)
    "2025.02.15",             # Random date (YYYY.MM.DD)
    "2023.09.15",             # Random date (YYYY.MM.DD)
    "2024.04.10",             # Random date (YYYY.MM.DD)
    "2023.02.28",             # Non-leap year date (YYYY.MM.DD)
    "2023.01.01",             # New Year's Day (YYYY.MM.DD)
    "2025.05.21",             # Random date (YYYY.MM.DD)
]

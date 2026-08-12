"""
THis is opposite to the valid_employee.py file. This is an invalid employee data file.

This file contains invalid employee data for testing purposes.
"""

invalid_employee_slash_dates = [
    {
        "name": "Alice Johnson",
        "hired_date": "2022/05/12 09:00:00+00:00"  # missing 'T'
    },
    {
        "name": "Brian Smith",
        "hired_date": "2023/01/20T14-30-00+00:00"   # wrong separator for time
    },
    {
        "name": "Carla Diaz",
        "hired_date": "2021/11/03T08:45:00+0000"    # missing ':' in timezone
    },
    {
        "name": "David Lee",
        "hired_date": "2024/15/03T10:15:00+00:00"   # invalid month-day (15 as month)
    },
    {
        "name": "Eva Martin",
        "hired_date": "2022/08/09T16:00:00Z "       # extra space at the end
    },
]

invalid_employee_dot_dates = [
    {
        "name": "Felix Turner",
        "hired_date": "2023.04.01T09:00+00:00"      # missing seconds
    },
    {
        "name": "Grace Park",
        "hired_date": "2022-12-11T14:30:00+00:00"   # wrong separator (dash instead of dot)
    },
    {
        "name": "Hassan Ali",
        "hired_date": "2021.07.23T08:45:00+24:00"   # invalid timezone (+24:00 not valid)
    },
    {
        "name": "Isabella Rossi",
        "hired_date": "2024.02.19T25:15:00+00:00"   # invalid hour (25)
    },
    {
        "name": "Jack Wilson",
        "hired_date": "2022.06.31T16:00:00+00:00"   # June 31st doesn't exist
    },
]

invalid_employee_dash_dates = [
    {
        "name": "Karen Müller",
        "hired_date": "2023-09-10T09:00:00+0000"    # missing ':' in timezone
    },
    {
        "name": "Liam O'Connor",
        "hired_date": "2022/10/05T14:30:00+00:00"   # wrong separator (slash instead of dash)
    },
    {
        "name": "Mia Chen",
        "hired_date": "2021-05-27 08:45:00+00:00"   # missing 'T'
    },
    {
        "name": "Noah Patel",
        "hired_date": "2024-01-08T10:15:00+99:99"   # totally invalid timezone
    },
    {
        "name": "Olivia Brown",
        "hired_date": "2022-03-18T16:00+00:00"      # missing seconds
    },
]


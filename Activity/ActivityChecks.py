from datetime import timedelta
import numpy as np


def check_if_timedelta_greater_than_minimum_days(time_difference: timedelta, min_days: int) -> bool:
    """Check if timedelta greater than a minimum number of days"""
    if time_difference > timedelta(days=min_days):
        return True
    else:
        return False


def check_activity_bigger_than_value_and_assign_to_nan(row, max_mileage: int = 20000):
    if row['Activity'] > max_mileage:
        return np.nan
    else:
        return row['Activity']

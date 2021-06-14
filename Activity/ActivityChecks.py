from datetime import timedelta
import numpy as np
import pandas as pd
from typing import Dict


def check_if_timedelta_greater_than_minimum_days(time_difference: timedelta, min_days: int) -> bool:
    """Check if timedelta greater than a minimum number of days"""
    if time_difference > timedelta(days=min_days):
        return True
    else:
        return False


def calculate_activity_outliers_thresholds(categorized_vehicles_df: pd.DataFrame) -> Dict:
    """Calculates outliers with the IQR method for each category and returns a dictionary with the min and max values"""

    CATEGORIES = ['Passenger Cars', 'Light Commercial Vehicles', 'Heavy Duty Trucks',
                  'Buses', 'L-Category']
    activity_outliers_per_category_mapping = {
        'Passenger Cars': {'Min_Activity': 0, 'Max_Activity': 0},
        'Light Commercial Vehicles': {'Min_Activity': 0, 'Max_Activity': 0},
        'L-Category': {'Min_Activity': 0, 'Max_Activity': 0},
        'Heavy Duty Trucks': {'Min_Activity': 0, 'Max_Activity': 0},
        'Buses': {'Min_Activity': 0, 'Max_Activity': 0},
        'Off Road': {'Min_Activity': 0, 'Max_Activity': 0}
    }

    for category in CATEGORIES:
        data = categorized_vehicles_df[(categorized_vehicles_df['Category'] == category) &
                                       (categorized_vehicles_df['Activity'].notna())]['Activity']
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        activity_outliers_per_category_mapping[category]['Max_Activity'] = q3 + 1.5 * iqr

        # Assign minimum to 1 if value of minimum activity to be outlier is negative
        if (q1 - 1.5 * iqr) < 0:
            activity_outliers_per_category_mapping[category]['Min_Activity'] = 1
        else:
            activity_outliers_per_category_mapping[category]['Min_Activity'] = q1 - 1.5 * iqr

    return activity_outliers_per_category_mapping


def check_for_activity_outliers(row: pd.Series, activity_outliers_per_category_mapping: Dict):
    """Assign to nan Activity outliers"""

    if row['Activity'] < activity_outliers_per_category_mapping[row['Category']]['Min_Activity']:
        return np.nan
    elif row['Activity'] > activity_outliers_per_category_mapping[row['Category']]['Max_Activity']:
        return np.nan
    else:
        return row['Activity']

# TODO:; print to file the vehicles with bigger activity
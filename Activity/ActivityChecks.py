from datetime import timedelta
import numpy as np
import pandas as pd
from typing import Dict
import logging

info_logger = logging.getLogger('info_logger' + '.ActivityChecks')


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
    lifetime_activity_outliers_per_category_mapping = {
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
        # calculate activity outliers
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        activity_outliers_per_category_mapping[category]['Max_Activity'] = q3 + 1.5 * iqr
        # Assign minimum to 250 if value of minimum activity to be outlier is less than 250
        if (q1 - 1.5 * iqr) < 250:
            activity_outliers_per_category_mapping[category]['Min_Activity'] = 250
        else:
            activity_outliers_per_category_mapping[category]['Min_Activity'] = q1 - 1.5 * iqr

        # calculate lifetime activity outliers
        data = categorized_vehicles_df[(categorized_vehicles_df['Category'] == category) &
                                       (categorized_vehicles_df['Lifetime Activity'].notna())]['Lifetime Activity']
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        lifetime_activity_outliers_per_category_mapping[category]['Max_Activity'] = q3 + 1.7 * iqr # 1.7 is equivalent to 3σ
        # Assign minimum to 250 if value of minimum activity to be outlier is less than 250
        if (q1 - 1.5 * iqr) < 250:
            lifetime_activity_outliers_per_category_mapping[category]['Min_Activity'] = 250
        else:
            lifetime_activity_outliers_per_category_mapping[category]['Min_Activity'] = q1 - 1.5 * iqr

    info_logger.info(f'Activity outliers per Category: ')
    info_logger.info((activity_outliers_per_category_mapping))

    return activity_outliers_per_category_mapping, lifetime_activity_outliers_per_category_mapping


def check_for_activity_outliers(row: pd.Series, activity_outliers_per_category_mapping: Dict,
                                lifetime_activity_outliers_per_category_mapping: Dict):
    """Assign to nan Activity and Lifetime Activity outliers"""

    activity = row['Activity']
    lifetime_activity = row['Lifetime Activity']

    # Check activity outliers
    if row['Activity'] < activity_outliers_per_category_mapping[row['Category']]['Min_Activity']:
        info_logger.info(f"Vehicle amb activitat inferior al llindar mínim: "
                         f"{activity_outliers_per_category_mapping[row['Category']]['Min_Activity']}")
        info_logger.info(row)
        activity = np.nan
    elif row['Activity'] > activity_outliers_per_category_mapping[row['Category']]['Max_Activity']:
        info_logger.info(f"Vehicle amb activitat superior al llindar màxim "
                         f"{activity_outliers_per_category_mapping[row['Category']]['Max_Activity']}: ")
        info_logger.info(row)
        activity = np.nan

    # Check Lifetime Activity outliers
    if row['Lifetime Activity'] < lifetime_activity_outliers_per_category_mapping[row['Category']]['Min_Activity']:
        info_logger.info(f"Vehicle amb Lifetime cumulative activity inferior al llindar mínim: "
                         f"{lifetime_activity_outliers_per_category_mapping[row['Category']]['Min_Activity']}")
        info_logger.info(row)
        lifetime_activity = np.nan
    elif row['Lifetime Activity'] > lifetime_activity_outliers_per_category_mapping[row['Category']]['Max_Activity']:
        info_logger.info(f"Vehicle amb Lifetime cumulative activity superior al llindar màxim "
                         f"{lifetime_activity_outliers_per_category_mapping[row['Category']]['Max_Activity']}: ")
        info_logger.info(row)
        lifetime_activity = np.nan

    return activity, lifetime_activity


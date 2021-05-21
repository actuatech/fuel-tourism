import numpy as np
import pandas as pd
from datetime import timedelta, datetime

from .ActivityChecks import check_if_timedelta_greater_than_minimum_days

DAYS_IN_A_YEAR = 365


def time_between_dates(date1: datetime, date2: datetime) -> timedelta:
    """Take two dates and return the time difference between them. """
    try:
        timedelta_between_dates = date1 - date2
        return timedelta_between_dates
    except Exception as e:
        print(f'Unable to compare date1 and date2. Error: {e}')


def activity_time_and_km_between_itv_revisions(row, max_date: datetime, min_days_between_revisions: int = 300) -> int:
    """
    Calculate the time in days between 2 consecutives itv revisions and the corresponding mileage.
     Only if:
        - the revisions are separated by a minimum number of days (avoiding therefore revisions not passed)
        If not, takes the next consecutives revisions into account and so on until last revisions is reached.
        - the revisions are made before a given date (to avoid for example post covid activity paterns)

    :param row: vehicle pd.Serie from register dataframe
    :param max_date: max date to take into account
    :param min_days_between_revisions: minimum number of days between revisions
    :return: tuple (number of days between revisions, mileage between those revisions in Km, activity in km/year)
    """
    if pd.notna(row['DATA_DARRERA_ITV']) and row['DATA_DARRERA_ITV'] < max_date:
        if pd.notna(row['DATA_DARRERA_ITV2']) and row['DATA_DARRERA_ITV2'] < max_date:
            timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV'], row['DATA_DARRERA_ITV2'])

            if check_if_timedelta_greater_than_minimum_days(timedelta_revisions, min_days_between_revisions):
                mileage = row['KM_DARRERA_ITV'] - row['KM_DARRERA_ITV2']
                if mileage > 0:
                    activity = (mileage / timedelta_revisions.days) * DAYS_IN_A_YEAR
                    return timedelta_revisions.days, mileage, abs(activity)
                else:
                    print('Error de kilometratge: ')
                    print(row)
                    print('-')
            else:
                if pd.notna(row['DATA_DARRERA_ITV3']) and row['DATA_DARRERA_ITV3'] < max_date:
                    timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV2'], row['DATA_DARRERA_ITV3'])

                    if check_if_timedelta_greater_than_minimum_days(timedelta_revisions, min_days_between_revisions):
                        mileage = row['KM_DARRERA_ITV2'] - row['KM_DARRERA_ITV3']
                        if mileage > 0:
                            activity = (mileage / timedelta_revisions.days) * DAYS_IN_A_YEAR
                            return timedelta_revisions.days, mileage, activity
                        else:
                            print('Error de kilometratge: ')
                            print(row)
                            print('-')
                    else:
                        if pd.notna(row['DATA_DARRERA_ITV4']) and row['DATA_DARRERA_ITV4'] < max_date:
                            timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV3'], row['DATA_DARRERA_ITV4'])

                            if check_if_timedelta_greater_than_minimum_days(timedelta_revisions,
                                                                            min_days_between_revisions):
                                mileage = row['KM_DARRERA_ITV3'] - row['KM_DARRERA_ITV4']
                                if mileage > 0:
                                    activity = (mileage / timedelta_revisions.days) * DAYS_IN_A_YEAR
                                    return timedelta_revisions.days, mileage, activity
                                else:
                                    print('Error de kilometratge: ')
                                    print(row)
                                    print('-')
                            else:
                                if pd.notna(row['DATA_DARRERA_ITV5']) and row['DATA_DARRERA_ITV5'] < max_date:
                                    timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV4'],
                                                                             row['DATA_DARRERA_ITV5'])

                                    if check_if_timedelta_greater_than_minimum_days(timedelta_revisions,
                                                                                    min_days_between_revisions):
                                        mileage = row['KM_DARRERA_ITV4'] - row['KM_DARRERA_ITV5']
                                        if mileage > 0:
                                            activity = (mileage / timedelta_revisions.days) * DAYS_IN_A_YEAR
                                            return timedelta_revisions.days, mileage, activity
                                        else:
                                            print('Error de kilometratge: ')
                                            print(row)
                                            print('-')
                                    else:
                                        return np.nan, np.nan, np.nan

    return np.nan, np.nan, np.nan

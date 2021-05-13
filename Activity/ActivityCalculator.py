from datetime import timedelta, datetime


# TODO eliminar 2020. S'ha de veure tema itv intermitja. març 2020 limit. km de 2018 i 2019
# columna days, km, activity pel vehicle, mitjana per categoria.
# per cada categoria; hoistograma mitja, mitjana, desviacio per l'activitat'
# filtre per data anterior
import pandas as pd


def time_between_dates(date1: datetime, date2: datetime) -> timedelta:
    """Take two dates and return the time difference between them. """
    try:
        timedelta_between_dates = date1 - date2
        return timedelta_between_dates
    except Exception as e:
        print(f'Unable to compare date1 and date2. Error: {e}')


def check_if_timedelta_greater_than_minimum_days(time_difference: timedelta, min_days: int) -> bool:
    """Check if timedelta greater than a minimum number of days"""
    if time_difference > timedelta(days=min_days):
        return True
    else:
        return False


def time_between_itv_revisions(row, min_days_between_revisions: int = 330) -> int:
    """Return the time in days between 2 consecutives itv revisions, if those revisions are separated by a min time"""

    if pd.notna(row['DATA_DARRERA_ITV']):  # If there is a itv revision
        if pd.notna(row['DATA_DARRERA_ITV2']):  # If there is a second itv revision
            timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV'], row['DATA_DARRERA_ITV2'])
            if check_if_timedelta_greater_than_minimum_days(timedelta_revisions, min_days_between_revisions):
                return timedelta_revisions.days
            else:
                timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV2'], row['DATA_DARRERA_ITV3'])
                if check_if_timedelta_greater_than_minimum_days(timedelta_revisions, min_days_between_revisions):
                    return timedelta_revisions.days
                else:
                    print('Vehicle with TWO revisions very close to the previous one ')
                    print('row')
                    print('-')
                    timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV3'], row['DATA_DARRERA_ITV4'])
                    if check_if_timedelta_greater_than_minimum_days(timedelta_revisions, min_days_between_revisions):
                        return timedelta_revisions.days
                    else:
                        print('Vehicle with THREE revisions very close to the previous one ')
                        print('row')
                        print('-')
                        timedelta_revisions = time_between_dates(row['DATA_DARRERA_ITV4'], row['DATA_DARRERA_ITV5'])
                        if check_if_timedelta_greater_than_minimum_days(timedelta_revisions,
                                                                        min_days_between_revisions):
                            return timedelta_revisions.days
                        else:
                            print('Vehicle with FOUR revisions very close to the previous one ')
                            print('row')
                            print('-')
                            return None
        else:
            return None
    else:
        return None

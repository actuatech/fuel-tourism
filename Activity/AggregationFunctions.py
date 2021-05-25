from typing import List
import pandas as pd


def groupby_partitions(vehicles_df: pd.DataFrame, partitions: List) -> pd.DataFrame.groupby:
    """
    Group the vehicles register Dataframe into the given partitions
    Calculates the sum for the column COUNT (number of vehicles in the given aggregation)
    Calculates the Mean of the column Activity for the given aggregation

    :param vehicles_df: with columns: ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Num_of_days', 'Mileage',
     'Activity', 'COUNT']
    :param partitions: must be one or more of :  ['Category', 'Fuel', 'Segment', 'Euro Standard']
    :return: grouped pd.Dataframe for the given partitions
    """
    NUM_OF_DAYS_PER_YEAR = 365
    try:
        groupby = vehicles_df.groupby(
            partitions, dropna=False, as_index=False).agg(
            {'Activity': 'mean', 'COUNT': 'sum', 'Mileage': 'sum', 'Num_of_days': 'sum'}).rename(
            {'Activity': 'Mean_Activity'}, axis=1)

    except Exception:
        raise Exception(f'Unable to groupby {partitions}, the vehicles dataframe')

    return groupby


def filter_groupby_partitions(groupby: pd.DataFrame.groupby, row: pd.Series, euro_standard: str)\
        -> pd.DataFrame.groupby:
    """
    Filters the groupby dataframe to match the values of the given row for the partitions:
    :param groupby: grouped vehicles dataframe
    :param row: row of the vehicles dataframe
    :param euro_standard: Value of the second last Euro Standard for the row(vehicle) Category
    :return: Groupby with matching values for the given partitions
    """
    partitions = groupby.columns.tolist()
    filtered_groupby = groupby.copy()
    if 'Euro Standard' in partitions:
        if euro_standard:
            filtered_groupby = filtered_groupby[(filtered_groupby['Euro Standard'] == euro_standard)]
        else:
            filtered_groupby = filtered_groupby[(filtered_groupby['Euro Standard'] == row['Euro Standard'])]
    if 'Category' in partitions:
        filtered_groupby = filtered_groupby[(filtered_groupby['Category'] == row['Category'])]
    if 'Segment' in partitions:
        filtered_groupby = filtered_groupby[(filtered_groupby['Segment'] == row['Segment'])]
    if 'Fuel' in partitions:
        filtered_groupby = filtered_groupby[(filtered_groupby['Fuel'] == row['Fuel'])]

    return filtered_groupby

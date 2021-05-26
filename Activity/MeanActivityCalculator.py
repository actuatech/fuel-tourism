import numpy as np
import pandas as pd
from typing import List, Dict

from .AggregationFunctions import groupby_partitions, filter_groupby_partitions
from .ActivityChecks import check_for_activity_outliers


def mean_activity_calculator(vehicles_df: pd.DataFrame, row: pd.Series, partitions: List, min_counts: int,
                             euro_standard: str = None) -> float:
    """
    Calculates the mean activity of the grouped dataframe given partitions and matching the values of the vehicles (row)
    For the cases where the Mean activty could not be calculated given the minimum counts

    :param vehicles_df: Full dataframe of the vehicles inventory, with columns:
            ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Num_of_days', 'Mileage', 'Activity', 'COUNT']
    :param row: row of vehicle dataframe representing a vehicle. With columns:
            ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Mileage', 'COUNT', 'Mean_Activity']

    :param partitions: must be one or more of :  ['Category', 'Fuel', 'Segment', 'Euro Standard']
    :param min_counts: minimum number of vehicles to be grouped within the given partitions to take the
    mean activity calculation as valid.
    :param euro_standard: Value of the second last Euro Standard for the row(vehicle) Category
    :return: The calculated mean activity for the corresponding grouping or np.nan if min_counts condition is not meet
    """

    # Grouping vehicles dataframe by given partitions and filter it to match partitions of the given row of Dataframe
    filtered_groupby = filter_groupby_partitions(groupby_partitions(vehicles_df, partitions), row, euro_standard)\
        .reset_index()

    if filtered_groupby.shape[0] != 1:  # The agrupation must contain just one row matching partitions of given row
        raise Exception(
            f"Filtered Groupby Dataframe to match segmentation {partitions}, with more or less than 1 row:"
            f" \n {filtered_groupby} \n for vehicle: \n {row}"
        )

    # Returns Mean Activity if the agrupation meets the minimum number of vehicles to trust the calculated value
    if filtered_groupby['COUNT'][0] >= min_counts:
        mean_activity = filtered_groupby['Mean_Activity'][0]
        return mean_activity

    return np.nan


def mean_activity_calculator_by_grouping(row: pd.Series, vehicles_df: pd.DataFrame,
                                         mapping_category_last_euro_standard: Dict, min_counts: int = 100) -> float:
    """
    Calculates the mean activity for a given vehicle (row) by grouping it and returns the mean activity of the group
    if the grouping has a minimum of stock.
    There is a sequential grouping, with priorities on Category, Fuel, Euro Standard and Segment.

    :param row: row of the stock (pd.Dataframe.groupby), it is an aggregation of vehicles with columns
     ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Num_of_days', 'Mileage', 'COUNT', 'Mean_Activity']
    :param vehicles_df: categorized Dataframe of the vehicles fleet
    :param mapping_category_last_euro_standard: dict that maps each category with it's last realeased Euro Standard
    :param min_counts: minimum stock size to take the resulting mean activity of the agrupation as valid
    :return: Mean activity of the agrupation that first matches the minimum stock required to assigned to the given row
    """

    row_euro_standard_mapping = mapping_category_last_euro_standard[row['Category']]

    if row['Category'] in CATEGORIES:
        if (row['COUNT'] < min_counts or row['Mileage'] == 0) and pd.notna(row['Euro Standard']):

            # For vehicles not in last Euro Standard group, Agregation by Category, Fuel and Euro Standard
            if row['Euro Standard'] != row_euro_standard_mapping['last_euro']:
                partitions = ['Category', 'Fuel', 'Euro Standard']
                mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
                if pd.notna(mean_activity):
                    print(f'Mean activity with aggregation by Category, Fuel and Euro Standard assigned to: \n {row}')
                    return round(mean_activity, 0)

            # Assigning the Mean Activity of the previous Euro Standard (for new vehicles with no ITV mileage info)
            else:
                assigned_euro_standard = row_euro_standard_mapping['second_last_euro']
                partitions = ['Category', 'Fuel', 'Segment', 'Euro Standard']
                mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts,
                                                         assigned_euro_standard)
                if pd.notna(mean_activity):
                    print(f'Mean activity taken from previous Euro Standard assigned to \n {row}')
                    return round(mean_activity, 0)
                # Assigning the Mean Activity of the previous Euro Standard and NO Fuel aggregation
                    # for new vehicles with no ITV mileage info
                partitions = ['Category', 'Segment', 'Euro Standard']
                mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts,
                                                         assigned_euro_standard)
                if pd.notna(mean_activity):
                    print(f'Mean activity taken from previous Euro Standard, with no fuel aggregation assigned to:'
                          f' \n {row}')
                    return round(mean_activity, 0)

            # Aggregation by Category, Fuel, Segment
            partitions = ['Category', 'Fuel', 'Segment']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity with aggregation by Category, Fuel and Segment assigned to: \n {row}')
                return round(mean_activity, 0)

            # For minoritary fuel types like hybrid and PHEV, aggregation by fuel is dropped
            if (row['Fuel'] in HYBRID_PHEV_TYPES) and (row['Euro Standard'] != row_euro_standard_mapping['last_euro'])\
                    and (row['Category'] != 'L-Category'):
                partitions = ['Category', 'Segment', 'Euro Standard']
                mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
                if pd.notna(mean_activity):
                    print(f'Mean activity with aggregation by Category, Segment and Euro Standard assigned to '
                          f'minoritary fuel vehicle: \n {row}')
                    return round(mean_activity, 0)

            # Just group by Segment and Category
            partitions = ['Category', 'Segment']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity with aggregation by Category and Segment assigned to vehicle: \n {row}')
                return round(mean_activity, 0)

            # Just group by Fuel and Category
            partitions = ['Category', 'Fuel']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity with aggregation by Category and Fuel assigned to vehicle:'
                      f' \n {row}')
                return round(mean_activity, 0)

            # If previous partitions are not enough, just group by Category
            partitions = ['Category']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity just aggregating by Category, assigned to vehicle: \n {row}')
                return mean_activity

        # Electrical vehicles (No Euro Standard) with no minimal COUNTS per segment
        elif row['Fuel'] == 'Battery electric' and pd.isna(row['Mean_Activity']):
            partitions = ['Category', 'Segment']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity aggregating by Category and Segment assigned to  electrical vehicle: \n {row}')
                return round(mean_activity, 0)

        # Vehicles with no Euro Standard
        elif pd.isna(row['Euro Standard']) and pd.isna(row['Mean_Activity']):
            partitions = ['Category', 'Fuel', 'Segment']
            mean_activity = mean_activity_calculator(vehicles_df, row, partitions, min_counts)
            if pd.notna(mean_activity):
                print(f'Mean activity NOT aggregating by Euro Standard assigned to \n {row}')
                return round(mean_activity, 0)

        else:
            if pd.notna(row['Mean_Activity']):  # Keep Category/Fuel/Segment/Euro previously calculated mean activity
                return row['Mean_Activity']
            else:
                print(f'!!! Unable to calculate Mean_Activity for:  \n {row} ')
    else:
        raise Exception(f'Category type not found for vehicle: \n {row} \n')


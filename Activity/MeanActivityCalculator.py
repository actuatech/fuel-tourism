import numpy as np
import pandas as pd
from typing import List, Dict
import logging

from .AggregationFunctions import groupby_partitions, filter_groupby_partitions
from .ActivityChecks import check_for_activity_outliers
from Classification.MappingConstants import CATEGORIES, HYBRID_PHEV_TYPES

info_logger = logging.getLogger('info_logger' + '.MeanActivityCalculator')
logger = logging.getLogger('logger' + '.MeanActivityCalculator')


def activity_stats_calculator(vehicles_df: pd.DataFrame, row: pd.Series, partitions: List, min_stock: int,
                              euro_standard: str, fuel_type: str) -> float:
    """
    Calculates the mean activity of the grouped dataframe given partitions and matching the values of the vehicles (row)
    For the cases where the Mean activty could not be calculated given the minimum stock

    :param vehicles_df: Full dataframe of the vehicles inventory, with columns:
            ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Num_of_days', 'Mileage', 'Activity', 'Stock']
    :param row: row of vehicle dataframe representing a vehicle. With columns:
            ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Mileage', 'Stock', 'Mean_Activity']

    :param partitions: must be one or more of :  ['Category', 'Fuel', 'Segment', 'Euro Standard']
    :param min_stock: minimum number of vehicles to be grouped within the given partitions to take the
    mean activity calculation as valid.
    :param euro_standard: Value of the second last Euro Standard for the row(vehicle) Category
    :param fuel_type: Value of the Fuel type to filter on
    :return: The calculated activity statistics for the corresponding grouping or np.nan if min_stock condition not meet
    """

    # Grouping vehicles dataframe by given partitions and filter it to match partitions of the given row of Dataframe
    filtered_groupby = filter_groupby_partitions(
        groupby_partitions(vehicles_df, partitions), row, euro_standard, fuel_type
    ).reset_index()

    if filtered_groupby.shape[0] < 1:  # The agrupation must contain just one row matching partitions of given row
        logger.info(f"Filtered Groupby Dataframe to match segmentation {partitions}, with more or less than 1 row:"
                     f" {filtered_groupby} \n for vehicle: {row}", exc_info=True)
    elif filtered_groupby.shape[0] > 1:
        logger.warning(f"Filtered Groupby Dataframe to match segmentation {partitions}, with more or less than 1 row:"
                    f" {filtered_groupby} \n for vehicle: {row}", exc_info=True)
    # Returns Mean Activity if the agrupation meets the minimum number of vehicles to trust the calculated value
    if filtered_groupby['Notna_Count'][0] >= min_stock:
        mean_activity = filtered_groupby['Mean_Activity'][0]
        min_activity = filtered_groupby['Min_Activity'][0]
        max_activity = filtered_groupby['Max_Activity'][0]
        std_activity = filtered_groupby['Std_Activity'][0]
        mean_lifetime_activity = filtered_groupby['Mean_Lifetime_Activity'][0]

        return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

    return np.nan, np.nan, np.nan, np.nan, np.nan


def activity_stats_calculator_by_grouping(row: pd.Series, vehicles_df: pd.DataFrame,
                                          mapping_category_last_euro_standard: Dict, min_stock: int = 50) -> float:
    """
    Calculates the mean activity for a given vehicle (row) by grouping it and returns the mean activity of the group
    if the grouping has a minimum of stock.
    There is a sequential grouping, with priorities on Category, Fuel, Euro Standard and Segment.

    :param row: row of the stock (pd.Dataframe.groupby), it is an aggregation of vehicles with columns
     ['Category', 'Fuel', 'Segment', 'Euro Standard', 'Num_of_days', 'Mileage', 'Stock', 'Mean_Activity']
    :param vehicles_df: categorized Dataframe of the vehicles fleet
    :param mapping_category_last_euro_standard: dict that maps each category with it's last realeased Euro Standard
    :param min_stock: minimum stock size to take the resulting mean activity of the agrupation as valid
    :return: Mean activity statisitcs of the agrupation that first matches the minimum stock required to assigned to
     the given row
    """
    assigned_fuel = row['Fuel']
    assigned_euro_standard = row['Euro Standard']
    partitions = ['Category', 'Fuel', 'Segment', 'Euro Standard']
    if row['Category'] != 'Off Road':
        row_euro_standard_mapping = mapping_category_last_euro_standard[row['Category']]

    if row['Category'] in CATEGORIES:
        if (row['Notna_Count'] < min_stock or row['Mileage'] == 0) and pd.notna(row['Euro Standard']):
            # Assigning similar Fuel type for Hybrid and PHEV vehicles
            if row['Fuel'] in HYBRID_PHEV_TYPES:
                if row['Fuel'] == 'Petrol Hybrid' or row['Fuel'] == 'Petrol PHEV':
                    assigned_fuel = 'Petrol'
                elif row['Fuel'] == 'Diesel Hybrid' or row['Fuel'] == 'Diesel PHEV':
                    assigned_fuel = 'Diesel'
            # Assigning previous Euro Standard (for new vehicles with no ITV mileage info)
            if row['Euro Standard'] == row_euro_standard_mapping['last_euro'] or\
                    row['Euro Standard'] == row_euro_standard_mapping['second_last_euro']:

                assigned_euro_standard = row_euro_standard_mapping['second_last_euro']
                try:
                    mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                        vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
                except:
                    mean_activity = np.nan
                if pd.notna(mean_activity):
                    info_logger.info(f'Mean activity taken from previous Euro Standard assigned to: ')
                    info_logger.info(row)
                    return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

                assigned_euro_standard = row_euro_standard_mapping['third_last_euro']
                # Assigning third previous Euro Standard (for new vehicles with no ITV mileage info)
                try:
                    mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                        vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
                except:
                    mean_activity = np.nan
                if pd.notna(mean_activity):
                    info_logger.info(f'Mean activity taken from Third previous Euro Standard assigned to :')
                    info_logger.info(row)
                    return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity
                assigned_euro_standard = row_euro_standard_mapping['second_last_euro']

            # Aggregation by Category, Fuel, Segment
            partitions = ['Category', 'Fuel', 'Segment']
            try:
                mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                    vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            except:
                mean_activity = np.nan
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity with aggregation by Category, Fuel and Segment assigned to: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

            # Aggregation by Category, Fuel, Euro Standard
            partitions = ['Category', 'Fuel', 'Euro Standard']
            try:
                mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                    vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            except:
                mean_activity = np.nan
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity with aggregation by Category, Fuel and Euro Standard assigned to: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

            # Just group by Fuel and Category
            partitions = ['Category', 'Fuel']
            try:
                mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                    vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            except:
                mean_activity = np.nan
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity with aggregation by Category and Fuel assigned to vehicle: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

            # Just group by Segment and Category
            partitions = ['Category', 'Segment']
            try:
                mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                    vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            except:
                mean_activity = np.nan
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity with aggregation by Category and Segment assigned to vehicle: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

            # If previous partitions are not enough, just group by Category
            partitions = ['Category']
            try:
                mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                    vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            except:
                mean_activity = np.nan
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity just aggregating by Category, assigned to vehicle: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

        # Electrical vehicles (No Euro Standard) with no minimal stock per segment
        elif row['Fuel'] == 'Battery Electric' and pd.isna(row['Std_Activity']):
            partitions = ['Category']
            mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity = activity_stats_calculator(
                vehicles_df, row, partitions, min_stock, assigned_euro_standard, assigned_fuel)
            if pd.notna(mean_activity):
                info_logger.info(f'Mean activity aggregating by Category assigned to  electrical vehicle: ')
                info_logger.info(row)
                return mean_activity, min_activity, max_activity, std_activity, mean_lifetime_activity

        else:
            if pd.notna(row['Mean_Activity']):  # Keep Category/Fuel/Segment/Euro previously calculated mean activity
                return row['Mean_Activity'], row['Min_Activity'], row['Max_Activity'], row['Std_Activity'],\
                       row['Mean_Lifetime_Activity']
            elif row['Category'] == 'Off Road':
                return 0, 0, 0, 0, 0
            else:
                logger.error(f'!!! Unable to calculate Mean_Activity for:  \n {row} ', exc_info=True)
    else:
        raise logger.error(f'Category type not found for vehicle: \n {row} ', exc_info=True)


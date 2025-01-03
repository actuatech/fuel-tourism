# TODO: Preparar fitxer per fer que ingesta no peti en cas que les columnes del fitxer siguin diferents
# TODO: fitxer configuració

import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import os

from Logger import setup_logger
from Ingestion import register_ingestor_function
from DataCleaning import (
    filter_by_year_greater_or_equal_than,
    keep_row_if_na_in_column,
    drop_vehicles_with_no_fuel_associated,
    filter_by_year_smaller_than,
    convert_to_integer_df_columns,
    print_info,
    save_to_csv_vehicles_with_erroneous_data
)
from Classification import (
    category_fuel_segment_euro_classification_wrapper_function,
    MAPPING_CATEGORY_LAST_EURO_STANDARD
)
from Activity import (
    activity_time_and_km_between_itv_revisions,
    check_for_activity_outliers,
    calculate_activity_outliers_thresholds,
    activity_stats_calculator_by_grouping
)
from Graphing import(
    euro_distribution_pie_charts,
    stock_per_category_pie_chart,
    stock_per_manufacturing_year_and_category_bar_charts,
    activity_horizontal_bar_chart
)
from settings import (
    path_registre_vehicles,
    MIN_YEAR,
    MAX_DATE,
    MIN_DAYS_BETWEEN_REVISIONS,
    MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION,
    COVID_MILEAGE_ACTIVE,
    COVID_START_DATE,
    OUTPUT_FOLDER,
    filename_output_categorized_vehicle_data,
    filename_output_stock_activity,
    filename_output_vehicles_per_manufactuing_year,
    filename_output_vehicles_per_registration_year
)

# Working directory
dirname = os.path.dirname(__file__)
# Define the current working directory
cwd = Path.cwd()

# Create and initialize loggers
os.makedirs(cwd / OUTPUT_FOLDER, exist_ok=True)
setup_logger('logger', (cwd / OUTPUT_FOLDER / 'debug.log'))
setup_logger('info_logger', (cwd / OUTPUT_FOLDER / 'info.log'), stream=False)

logger = logging.getLogger('logger')
info_logger = logging.getLogger('info_logger')

logger.info("Started")

# ----
# CODE
# ----
# LOADING DATA
itv_raw = register_ingestor_function(path_registre_vehicles)
info_logger.info(f'Total number of vehicles loaded: {itv_raw.shape[0]}')

# DATA CLEANING
# Keep only last 30 years of data
vehicles_last_30_years = filter_by_year_greater_or_equal_than(itv_raw, 'ANY_FABRICACIO', MIN_YEAR)
info_logger.info(f'Total number of vehicles from the last 30 years: {vehicles_last_30_years.shape[0]}')
vehicles_last_30_years = filter_by_year_smaller_than(vehicles_last_30_years, 'DATA_ALTA', MAX_DATE)
info_logger.info(f'Total number of vehicles from the last 30 years until today: {vehicles_last_30_years.shape[0]}')
# Keep only vehicles that are not decommissioned
vehicles_last_30_years_active_today = keep_row_if_na_in_column(vehicles_last_30_years, 'DATA_BAIXA')
info_logger.info(f'Total number of vehicles active today: {vehicles_last_30_years_active_today.shape[0]}')
# Drop vehicles with missing Fuel data
good_vehicles_df = drop_vehicles_with_no_fuel_associated(vehicles_last_30_years_active_today)
info_logger.info(f'Total number of vehicles taken into account: {good_vehicles_df.shape[0]}')


# CATEGORIZING VEHICLES
categorized_vehicles_df = category_fuel_segment_euro_classification_wrapper_function(good_vehicles_df)

# Create columns Mileage, number of days and corresponding Activity for each vehicle
categorized_vehicles_df['Num_of_days'], categorized_vehicles_df['Mileage'], categorized_vehicles_df['Activity'], \
    categorized_vehicles_df['Lifetime Activity'] = zip(*categorized_vehicles_df.apply(
        lambda row: activity_time_and_km_between_itv_revisions(row, MAX_DATE, MIN_DAYS_BETWEEN_REVISIONS), axis=1))


# Assign to nan Activity outliers
activity_outliers_per_category_mapping, lifetime_activity_outliers_per_category_mapping =\
    calculate_activity_outliers_thresholds(categorized_vehicles_df)

# Save erroneous data to csv files
save_to_csv_vehicles_with_erroneous_data(categorized_vehicles_df, OUTPUT_FOLDER,
                                         activity_outliers_per_category_mapping,
                                         lifetime_activity_outliers_per_category_mapping)

categorized_vehicles_df['Activity'], categorized_vehicles_df['Lifetime Activity'] = zip(*categorized_vehicles_df.apply(
    lambda row: check_for_activity_outliers(row, activity_outliers_per_category_mapping,
                                            lifetime_activity_outliers_per_category_mapping), axis=1))

# Save cleaned, categorized data and vehicle activity to csv
print_info(categorized_vehicles_df) # print info
logger.info('Saving cleaned, categorized data and vehicle activity to csv')
categorized_vehicles_df.to_csv(filename_output_categorized_vehicle_data)

# Grouping per manufactuing year
veh_per_manuf_year_df = categorized_vehicles_df.groupby(['Category', 'Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False, as_index=False).agg(
        quantity=('ANY_FABRICACIO', 'count')).reset_index()
veh_per_manuf_year_df = veh_per_manuf_year_df.sort_values(by=['Category', 'Fuel', 'Segment', 'ANY_FABRICACIO'], ascending=True)
veh_per_manuf_year_df.to_csv(filename_output_vehicles_per_manufactuing_year, index=False)

# Grouping per registration year
veh_per_reg_year_df = categorized_vehicles_df.copy()
veh_per_reg_year_df['DATA_ALTA'] = veh_per_reg_year_df['DATA_ALTA'].dt.year
veh_per_reg_year_df = veh_per_reg_year_df.groupby(['Category', 'Fuel', 'Segment', 'DATA_ALTA'], dropna=False, as_index=False).agg(
        quantity=('DATA_ALTA', 'count')).reset_index()
veh_per_reg_year_df = veh_per_reg_year_df.sort_values(by=['Category', 'Fuel', 'Segment', 'DATA_ALTA'], ascending=True)
veh_per_reg_year_df.to_csv(filename_output_vehicles_per_registration_year, index=False)


# Create Stock Column
categorized_vehicles_df['Stock'] = 1

# STOCK CONFIGURATION
stock_df = categorized_vehicles_df.groupby(
            ['Category', 'Fuel', 'Segment', 'Euro Standard'], dropna=False, as_index=False).agg(Stock=('Stock', 'sum'))

# Filter categorized dataframe to delete vehicles that has revision after COVID_START_DATE
if COVID_MILEAGE_ACTIVE:
    categorized_vehicles_df_before_covid = filter_by_year_smaller_than(categorized_vehicles_df,
                                                                       'DATA_DARRERA_ITV', COVID_START_DATE)
else:
    categorized_vehicles_df_before_covid = categorized_vehicles_df

# Statistics calculation
mileage_df = categorized_vehicles_df_before_covid.groupby(
    ['Category', 'Fuel', 'Segment', 'Euro Standard'], dropna=False, as_index=False).agg(
    Mileage=('Mileage', 'sum'),
    Min_Activity=('Activity', 'min'),
    Max_Activity=('Activity', 'max'),
    Std_Activity=('Activity', 'std'),
    Mean_Activity=('Activity', 'mean'),
    Mean_Lifetime_Activity=('Lifetime Activity', 'mean'),
    Notna_Count=('Activity', 'count')
)

# Join stock configuration with associated mileage
stock_and_mileage_df = pd.merge(stock_df, mileage_df, on=['Category', 'Fuel', 'Segment', 'Euro Standard'], how='left')
stock_and_mileage_df['Notna_Count'].fillna(0, inplace=True)

# Calculate stadistics for categorizations that do not have enough data, by grouping
stats_df = stock_and_mileage_df.apply(
    lambda row: activity_stats_calculator_by_grouping(
        row, categorized_vehicles_df, MAPPING_CATEGORY_LAST_EURO_STANDARD, MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION)
    , result_type='expand', axis='columns').rename(columns={0: 'Mean_Activity',
                                                            1: 'Min_Activity',
                                                            2: 'Max_Activity',
                                                            3: 'Std_Activity',
                                                            4: 'Mean_Lifetime_Activity',
                                                            }
                                                  )
# Join stock with updated activity statistics
stock_and_mileage_df = pd.concat(
    [stock_and_mileage_df.drop(['Mean_Activity', 'Min_Activity', 'Max_Activity', 'Std_Activity',
                                'Mean_Lifetime_Activity'], axis=1), stats_df],
    axis='columns')

# Convert activity statistics columns to integer and check for nan values
convert_to_integer_df_columns(stock_and_mileage_df)

logger.info('Saving stock and activity to csv')
stock_and_mileage_df.drop(['Notna_Count'], axis=1).to_csv(filename_output_stock_activity)
logger.info(f'Number of categories: {stock_and_mileage_df.shape[0]}')
# Save wanted results
logger.info('Loading charts')
stock_per_category_pie_chart(categorized_vehicles_df, OUTPUT_FOLDER)
euro_distribution_pie_charts(categorized_vehicles_df, OUTPUT_FOLDER)
stock_per_manufacturing_year_and_category_bar_charts(categorized_vehicles_df, OUTPUT_FOLDER)
activity_horizontal_bar_chart(stock_and_mileage_df, OUTPUT_FOLDER)
logger.info('end')

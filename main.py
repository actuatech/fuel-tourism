# TODO: Preparar fitxer per fer que ingesta no peti en cas que les columnes del fitxer siguin diferents
# TODO: no tenir en compte activitat per sobre el 15 de març del 2020

import pandas as pd
from pathlib import Path
from datetime import datetime

from Ingestion import register_ingestor_function
from DataCleaning import (
    filter_by_year_greater_or_equal_than,
    keep_row_if_na_in_column,
    drop_vehicles_with_no_fuel_associated,
    filter_by_year_smaller_than
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
    stock_per_manufacturing_year_and_category_bar_charts
)

# ----------
# PARAMETERS
# ----------
# ITV original data filename (Parameter)
filename_registre_vehicles = '01FEB2021_Historic_vehicles_amb_ITVs.xlsx'

# 01FEB2021_Historic_vehicles_amb_ITVs
# Years between from which data is keeped
MIN_YEAR = 1990
MAX_DATE = datetime(2021, 1, 1)

MIN_DAYS_BETWEEN_REVISIONS = 300
MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION = 50  # Min numb of vehicles in a given grouping to take the mean activity valid

# To keep current stock but calculate activity before covid date
COVID_MILEAGE_ACTIVE = True
COVID_START_DATE = datetime(2020, 3, 1)

# Output folder for results:
output_folder = '/Users/nilcelisfont/dev/fuel-turism/ouput/'

# Output filename of cleaned and categorized data:
filename_output_categorized_vehicle_data = output_folder + f'Registre_vehicles_{datetime.now().date()}.csv'
# Output filename for stock and activity dataframe
filename_output_stock_activity = output_folder + f'stock_activity_2019_{datetime.now().date()}.csv'

# ----
# CODE
# ----

# Define the current working directory
cwd = Path.cwd()
path_registre_vehicles = cwd / '_data' / filename_registre_vehicles



# LOADING DATA
print('Loading registre de vehicles')
itv_raw = register_ingestor_function(path_registre_vehicles)
print(f'Total number of vehicles loaded: {itv_raw.shape[0]}')
print('-')

# DATA CLEANING
print('Cleaning Data')
# Keep only last 30 years of data
vehicles_last_30_years = filter_by_year_greater_or_equal_than(itv_raw, 'ANY_FABRICACIO', MIN_YEAR)
vehicles_last_30_years = filter_by_year_smaller_than(vehicles_last_30_years, 'DATA_ALTA', MAX_DATE)
# Keep only vehicles that are not decommissioned
vehicles_last_30_years_active_today = keep_row_if_na_in_column(vehicles_last_30_years, 'DATA_BAIXA')
# Drop vehicles with missing Fuel data
good_vehicles_df = drop_vehicles_with_no_fuel_associated(vehicles_last_30_years_active_today)
print(f'Total number of vehicles taken into account: {good_vehicles_df.shape[0]}')
print('-')

# CATEGORIZING VEHICLES
print('Starting Vehicle Classification')
categorized_vehicles_df = category_fuel_segment_euro_classification_wrapper_function(good_vehicles_df)
categorized_vehicles_df_before_covid = filter_by_year_smaller_than(categorized_vehicles_df,
                                                                   'DATA_DARRERA_ITV', COVID_START_DATE)

# Create columns Mileage, number of days and corresponding Activity for each vehicle
categorized_vehicles_df['Num_of_days'], categorized_vehicles_df['Mileage'], categorized_vehicles_df['Activity'] = zip(
    *categorized_vehicles_df.apply(lambda row: activity_time_and_km_between_itv_revisions(
        row, MAX_DATE, MIN_DAYS_BETWEEN_REVISIONS), axis=1))

# Assign to nan Activity outliers
activity_outliers_per_category_mapping = calculate_activity_outliers_thresholds(categorized_vehicles_df)
categorized_vehicles_df['Activity'] = categorized_vehicles_df.apply(
    lambda row: check_for_activity_outliers(row, activity_outliers_per_category_mapping), axis=1)

# Save cleaned, categorized data and vehicle activity to csv
print('Saving cleaned, categorized data and vehicle activity to csv')
categorized_vehicles_df.to_csv(filename_output_categorized_vehicle_data)

# Create Stock Column
categorized_vehicles_df['Stock'] = 1
# STOCK CONFIGURATION
stock_df = categorized_vehicles_df.groupby(
            ['Category', 'Fuel', 'Segment', 'Euro Standard'], dropna=False, as_index=False).agg(Stock=('Stock', 'sum'))

# MILEAGE
if not COVID_MILEAGE_ACTIVE:
    categorized_vehicles_df_before_covid = categorized_vehicles_df

mileage_df = categorized_vehicles_df_before_covid.groupby(
    ['Category', 'Fuel', 'Segment', 'Euro Standard'], dropna=False, as_index=False).agg(
    Mileage=('Mileage', 'sum'),
    Min_Activity=('Activity', 'min'),
    Max_Activity=('Activity', 'max'),
    Std_Activity=('Activity', 'std'),
    Mean_Activity=('Activity', 'mean'),
    Notna_Count=('Activity', 'count')
)

# stock and mileage
stock_and_mileage_df = pd.merge(stock_df, mileage_df, on=['Category', 'Fuel', 'Segment', 'Euro Standard'], how='left')
stock_and_mileage_df['Notna_Count'].fillna(0, inplace=True)

stats_df = stock_and_mileage_df.apply(
    lambda row: activity_stats_calculator_by_grouping(
        row, categorized_vehicles_df, MAPPING_CATEGORY_LAST_EURO_STANDARD, MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION)
    , result_type='expand', axis='columns').rename(columns={0: 'Mean_Activity',
                                                            1: 'Min_Activity',
                                                            2: 'Max_Activity',
                                                            3: 'Std_Activity'}
                                                   )
stock_and_mileage_df = pd.concat(
    [stock_and_mileage_df.drop(['Mean_Activity', 'Min_Activity', 'Max_Activity', 'Std_Activity'], axis=1), stats_df],
    axis='columns')

try:
    stock_and_mileage_df['Mean_Activity'] = stock_and_mileage_df['Mean_Activity'].fillna(0).astype(int)
except ValueError:
    print('Check for nan values in the stock_and_mileage dataframe: Mean activity')

try:
    stock_and_mileage_df['Min_Activity'] = stock_and_mileage_df['Min_Activity'].fillna(0).astype(int)
except ValueError:
    print('Check for nan values in the stock_and_mileage dataframe: Min activity')

try:
    stock_and_mileage_df['Max_Activity'] = stock_and_mileage_df['Max_Activity'].fillna(0).astype(int)
except ValueError:
    print('Check for nan values in the stock_and_mileage dataframe: Max activity')

try:
    stock_and_mileage_df['Std_Activity'] = stock_and_mileage_df['Std_Activity'].fillna(0).astype(int)
except ValueError:
    print('Check for nan values in the stock_and_mileage dataframe: Standard deviation activity')

# Save wanted results
print('Loading charts')
stock_per_category_pie_chart(categorized_vehicles_df, output_folder)
euro_distribution_pie_charts(categorized_vehicles_df, output_folder)
stock_per_manufacturing_year_and_category_bar_charts(categorized_vehicles_df, output_folder)
print('end')

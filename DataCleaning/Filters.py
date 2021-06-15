from datetime import datetime
import pandas as pd


def filter_by_year_greater_or_equal_than(registre_df: pd.DataFrame, colname: str, date) -> pd.DataFrame:
    return registre_df[registre_df[colname] >= date]


def keep_row_if_na_in_column(registre_df: pd.DataFrame, colname: str) -> pd.DataFrame:
    return registre_df[registre_df[colname].isna()]


def drop_agricultural_vehicles(registre_df: pd.DataFrame) -> pd.DataFrame:
    num_agricultural_vehicles = registre_df[registre_df.CARBURANT == 'SENSE CARBURANT'].shape[0]
    print(f'Total number of agricultural vehicles deleted: {num_agricultural_vehicles}')
    return registre_df[registre_df['TIPUS'] != 'VEHICLES AGRICOLS']


def drop_vehicles_with_no_fuel_associated(registre_df: pd.DataFrame) -> pd.DataFrame:
    num_vehicles_no_fuel = registre_df[registre_df.CARBURANT == 'SENSE CARBURANT'].shape[0]
    print(f'Total number of vehicles with no fuel associated deleted: {num_vehicles_no_fuel}')
    return registre_df[registre_df['CARBURANT'] != 'SENSE CARBURANT']


def filter_by_year_smaller_than(registre_df: pd.DataFrame, colname: str, date) -> pd.DataFrame:
    return registre_df[registre_df[colname] < date]

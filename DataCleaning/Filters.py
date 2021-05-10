from datetime import datetime
import pandas as pd


def filter_by_year_greater_than(registre_df: pd.DataFrame, colname: str, date) -> pd.DataFrame:
    return registre_df[registre_df[colname] > date]


def drop_vehicles_agricols(registre_df: pd.DataFrame) -> pd.DataFrame:
    num_vehicles_agricols = registre_df[registre_df.CARBURANT == 'SENSE CARBURANT'].shape[0]
    print(f'Total number of vehicles agricols deleted: {num_vehicles_agricols}')
    return registre_df[registre_df['TIPUS'] != 'VEHICLES AGRICOLS']


def drop_vehicles_sense_carburant(registre_df: pd.DataFrame) -> pd.DataFrame:
    num_vehicles_sense_carburant = registre_df[registre_df.CARBURANT == 'SENSE CARBURANT'].shape[0]
    print(f'Total number of vehicles SENSE CARBURANT deleted: {num_vehicles_sense_carburant}')
    return registre_df[registre_df['CARBURANT'] != 'SENSE CARBURANT']

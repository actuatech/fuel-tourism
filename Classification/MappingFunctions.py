import pandas as pd
from .MappingConstants import CATEGORY_MAPPING_DICT, FUEL_MAPPING_DICT


def category_mapper_itv_copert(registre_df: pd.DataFrame) -> pd.DataFrame:
    """ Create column Category with corresponding category of the vehicle taken from original column TIPUS"""
    df = registre_df.copy()
    df['Category'] = df['TIPUS'].map(CATEGORY_MAPPING_DICT)  # Create new column Category
    return df


def fuel_mapper_itv_copert(registre_df: pd.DataFrame) -> pd.DataFrame:
    """ Create column Fuel with the fuel type of the vehicle taken from original column CARBURANT"""
    df = registre_df.copy()
    df['Fuel'] = df['CARBURANT'].map(FUEL_MAPPING_DICT)  # Create new column Fuel
    return df

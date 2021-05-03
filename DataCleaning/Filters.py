from datetime import datetime
import pandas as pd


def filter_by_year_greater_than(registres: pd.DataFrame, colname: str, date: datetime) -> pd.DataFrame:
    return registres[registres[colname] > date]

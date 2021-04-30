from datetime import datetime


def filter_by_year(registres: pd.DataFrame, colname: str) -> pd.DataFrame:
    return registres[registres[colname] > datetime(1990, 1, 1)]

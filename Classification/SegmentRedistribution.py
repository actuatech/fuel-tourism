import numpy as np
from .MappingConstants import CATEGORIES


def fill_nan_with_frequency(df, column_name):
    """ Fill na values of a given column with the normal distribution frequency for every Category    """
    for category in CATEGORIES:
        normal_distribution = df[df['Category'] == category][column_name].value_counts(normalize=True)
        df.loc[df[column_name].isna(), column_name] = np.random.choice(
            normal_distribution.index, p=normal_distribution.values, size=df[column_name].isna().sum())




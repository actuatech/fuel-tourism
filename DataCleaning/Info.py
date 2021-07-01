import pandas
import logging
from Classification import CATEGORIES

import pandas as pd

info_logger = logging.getLogger('info_logger' + '.ActivityCalculator')


def print_info(register_df: pd.DataFrame):
    number_of_vehicles_with_close_revision_dates = register_df[register_df.DATA_DARRERA_ITV2.notnull() &
                                                               register_df.Mileage.isnull()].shape[0]
    info_logger.info(f'Nombre de vehicles amb revisions ITV molt pròximes: {number_of_vehicles_with_close_revision_dates}')

    number_of_vehicles_with_null_CC_CM3_data = register_df[register_df['CC_CM3'].isna()].shape[0]
    info_logger.info(f'Nombre de vehicles sense dades de cilindrada CC_CM3: {number_of_vehicles_with_null_CC_CM3_data}')
    pass


def save_to_csv_vehicles_with_erroneous_data(register_df: pd.DataFrame, output_folder,
                                             activity_outliers_per_category_mapping,
                                             lifetime_activity_outliers_per_category_mapping):
    """ Save to csv files erroneous data"""

    df1 = register_df[(register_df['Category'] == 'Passenger Cars') &
                      ((register_df['CC_CM3'] < 560) | (register_df['CC_CM3'] > 8500))]
    df1.to_csv((output_folder + 'turismes_amb_dades_cilindrada_erronies.csv'))

    df2 = register_df[(register_df['Category'] == 'Buses') & (register_df['PES_BUIT'] > 18000)]
    df2.to_csv((output_folder + 'busos_amb_dades_pes_buit_erronies'))

    df3 = register_df[(register_df['Category'] == 'L-Category') & (register_df['CC_CM3'] < 40)]
    df3.to_csv((output_folder + 'motos_amb_dades_cm3_erronies.csv'))

    for i, category in enumerate(CATEGORIES):
        dfc = register_df[(register_df['Category'] == category) &
                          (register_df['Activity'] > activity_outliers_per_category_mapping[category]['Max_Activity'])]
        if i == 0:
            df = dfc.copy()
        elif i == (len(CATEGORIES) - 1):
            df.to_csv((output_folder + 'Vehicles_potencialment_amb_kilometratge_erroni.csv'))
        else:
            df = df.append(dfc)

    df4 = register_df[(register_df['KM_DARRERA_ITV'] < register_df['KM_DARRERA_ITV2']) |
                      (register_df['KM_DARRERA_ITV2'] < register_df['KM_DARRERA_ITV3']) |
                      (register_df['KM_DARRERA_ITV3'] < register_df['KM_DARRERA_ITV4'])]
    df4.to_csv((output_folder + 'Vehicles_amb_kilometrate_itv_anterior_menor.csv'))





import pandas
import logging

import pandas as pd

info_logger = logging.getLogger('info_logger' + '.ActivityCalculator')


def print_info(register_df: pd.DataFrame):
    number_of_vehicles_with_close_revision_dates = register_df[register_df.DATA_DARRERA_ITV2.notnull() &
                                                               register_df.Mileage.isnull()].shape[0]
    info_logger.info(f'Nombre de vehicles amb revisions ITV molt pròximes: {number_of_vehicles_with_close_revision_dates}')

    number_of_vehicles_with_null_CC_CM3_data = register_df[register_df['CC_CM3'].isna()].shape[0]
    info_logger.info(f'Nombre de vehicles sense dades de cilindrada CC_CM3: {number_of_vehicles_with_null_CC_CM3_data}')
    pass

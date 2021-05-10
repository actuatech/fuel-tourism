from datetime import datetime
import numpy as np


def date_parser(date: int) -> datetime:
    """ Parse DATA_ALTA and DATA-BAIXA columns of "Registre de vehicles Excel file"

    :param date: Date in format type %Y%m%d, ex: 19510915
    :return: datetime of the date or nan
    """

    date = str(date)
    try:
        result = datetime.strptime(date, '%Y%m%d')
        return result
    except ValueError as e:
        if date != 'nan':
            if date != '':
                try:
                    date = date[:4]
                    result = datetime.strptime(date, '%Y')
                    return result
                except ValueError:
                    print(f'Unable to parse date {date}, with function date_parser, error: {e}')
                    return date

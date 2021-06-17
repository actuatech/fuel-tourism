import pandas as pd
import numpy as np
import logging
from ordered_set import OrderedSet

from .DateParser import date_parser
from .YearParser import year_of_manufacturing_parser

COLUMNS_SET = OrderedSet(['TIPUS', 'ANY_FABRICACIO', 'DATA_ALTA', 'DATA_BAIXA',
                          'MARCA', 'MODEL', 'CARBURANT', 'KW', 'CV', 'CO2', 'UNITATS_CO2',
                          'CC_CM3', 'PES_BUIT',
                          'PES_TOTAL_MÀXIM', 'DATA_DARRERA_ITV', 'KM_DARRERA_ITV',
                          'DATA_DARRERA_ITV2', 'KM_DARRERA_ITV2', 'DATA_DARRERA_ITV3',
                          'KM_DARRERA_ITV3', 'DATA_DARRERA_ITV4', 'KM_DARRERA_ITV4',
                          'DATA_DARRERA_ITV5', 'KM_DARRERA_ITV5'])

logger = logging.getLogger('logger' + '.Ingestion')


def register_ingestor_function(path_registre_vehicles: str) -> pd.DataFrame:
    """
    Load Excel file to dataframe after checking correct columns names and data types
    :param path_registre_vehicles: path of Original Excel ITV register file
    :return: Dataframe of the file parsed to correct formats
    """
    # Load Excel file
    logger.info("Loading Excel file")
    try:
        registre = pd.read_excel(path_registre_vehicles, header=0)
    except Exception as e:
        logger.error(f'Not able to read Registres Excel File: {path_registre_vehicles}', exc_info=True)

    # Check Columns names
    if not COLUMNS_SET.issubset(set(registre.columns)):
        logger.warning(f'Nom de columnes diferents, pot donar problemes. Fitxer: {path_registre_vehicles}')
        logger.info(f'Columnes mínimes esperades: {COLUMNS_SET}')

    # Parsing of date columns
    try:
        registre['DATA_ALTA'] = registre['DATA_ALTA'].apply(date_parser)
    except KeyError:
        logger.error("No s'ha trobat columna DATA_ALTA", exc_info=True)
    try:
        registre['DATA_BAIXA'] = registre['DATA_BAIXA'].apply(date_parser)
    except KeyError:
        logger.error("No s'ha trobat columna DATA_BAIXA", exc_info=True)
    try:
        registre['DATA_DARRERA_ITV'] = registre['DATA_DARRERA_ITV'].apply(date_parser)
    except KeyError:
        logger.error(f"No s'ha trobat columna DATA_DARRERA_ITV al fitxer", exc_info=True)
    try:
        registre['DATA_DARRERA_ITV2'] = registre['DATA_DARRERA_ITV2'].apply(date_parser)
    except KeyError:
        logger.error(f"No s'ha trobat columna DATA_DARRERA_ITV2 al fitxer", exc_info=True)
    try:
        registre['DATA_DARRERA_ITV3'] = registre['DATA_DARRERA_ITV3'].apply(date_parser)
    except KeyError:
        logger.warning(f"No s'ha trobat columna DATA_DARRERA_ITV3 al fitxer")
    try:
        registre['DATA_DARRERA_ITV4'] = registre['DATA_DARRERA_ITV4'].apply(date_parser)
    except KeyError:
        logger.warning(f"No s'ha trobat columna DATA_DARRERA_ITV4 al fitxer")
    try:
        registre['DATA_DARRERA_ITV5'] = registre['DATA_DARRERA_ITV5'].apply(date_parser)
    except KeyError:
        logger.warning(f"No s'ha trobat columna DATA_DARRERA_ITV5 al fitxer")
    try:
        registre['ANY_FABRICACIO'] = registre['ANY_FABRICACIO'].apply(year_of_manufacturing_parser)
    except KeyError:
        logger.error("No s'ha trobat columna ANY_FABRICACIO", exc_info=True)

    registre['ANY_FABRICACIO'] = registre['ANY_FABRICACIO'].astype(pd.Int32Dtype())

    return registre

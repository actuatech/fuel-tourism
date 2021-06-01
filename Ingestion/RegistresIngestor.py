import pandas as pd
import numpy as np
from ordered_set import OrderedSet

from .DateParser import date_parser
from .YearParser import year_of_manufacturing_parser

COLUMNS_SET = OrderedSet(['TIPUS', 'MATRICULA', 'ANY_FABRICACIO', 'DATA_ALTA', 'DATA_BAIXA',
                          'MARCA', 'MODEL', 'CARBURANT', 'KW', 'CV', 'CO2', 'UNITATS_CO2',
                          'CC_CM3', 'PES_BUIT', 'CARREGA_UTIL', 'PES_TOTAL_RODANT',
                          'PES_TOTAL_MÀXIM', 'DATA_DARRERA_ITV', 'KM_DARRERA_ITV',
                          'DATA_DARRERA_ITV2', 'KM_DARRERA_ITV2', 'DATA_DARRERA_ITV3',
                          'KM_DARRERA_ITV3', 'DATA_DARRERA_ITV4', 'KM_DARRERA_ITV4',
                          'DATA_DARRERA_ITV5', 'KM_DARRERA_ITV5'])


def register_ingestor_function(path_registre_vehicles: str) -> pd.DataFrame:
    # Load Excel file
    try:
        registre = pd.read_excel(path_registre_vehicles, header=0)
    except Exception:
        raise Exception(f'Not able to ingest Registres Excel File: {path_registre_vehicles}')

    # Check Columns names
    if not COLUMNS_SET.issubset(set(registre.columns)):
        print(f'Nom de columnes diferents, pot donar problemes. Fitxer: {path_registre_vehicles}')
        print(f'Columnes esperades: {COLUMNS_SET}')

    # Parsing of date columns
    try:
        registre['DATA_ALTA'] = registre['DATA_ALTA'].apply(date_parser)
    except KeyError:
        print("No s'ha trobat columna DATA_ALTA")
    try:
        registre['DATA_BAIXA'] = registre['DATA_BAIXA'].apply(date_parser)
    except KeyError:
        raise Exception("No s'ha trobat columna DATA_BAIXA")
    try:
        registre['DATA_DARRERA_ITV'] = registre['DATA_DARRERA_ITV'].apply(date_parser)
    except KeyError:
        print(f"No s'ha trobat columna DATA_DARRERA_ITV al fitxer")
    try:
        registre['DATA_DARRERA_ITV2'] = registre['DATA_DARRERA_ITV2'].apply(date_parser)
    except KeyError:
        print(f"No s'ha trobat columna DATA_DARRERA_ITV2 al fitxer")
    try:
        registre['DATA_DARRERA_ITV3'] = registre['DATA_DARRERA_ITV3'].apply(date_parser)
    except KeyError:
        print(f"No s'ha trobat columna DATA_DARRERA_ITV3 al fitxer")
    try:
        registre['DATA_DARRERA_ITV4'] = registre['DATA_DARRERA_ITV4'].apply(date_parser)
    except KeyError:
        print(f"No s'ha trobat columna DATA_DARRERA_ITV4 al fitxer")
    try:
        registre['DATA_DARRERA_ITV5'] = registre['DATA_DARRERA_ITV5'].apply(date_parser)
    except KeyError:
        print(f"No s'ha trobat columna DATA_DARRERA_ITV5 al fitxer")
    try:
        registre['ANY_FABRICACIO'] = registre['ANY_FABRICACIO'].apply(year_of_manufacturing_parser)
    except KeyError:
        raise Exception("No s'ha trobat columna ANY_FABRICACIO")

    return registre

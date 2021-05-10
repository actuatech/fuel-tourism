import pandas as pd
import numpy as np

from .DateParser import date_parser
from .YearParser import year_of_manufacturing_parser

COLUMNS_SET = {'ANY_FABRICACIO', 'CARBURANT', 'CARREGA_UTIL', 'CC_CM3', 'CO2', 'CV', 'DATA_ALTA', 'DATA_BAIXA',
               'DATA_DARRERA_ITV', 'DATA_DARRERA_ITV2', 'DATA_DARRERA_ITV3', 'DATA_DARRERA_ITV4', 'DATA_DARRERA_ITV5',
               'KM_DARRERA_ITV', 'KM_DARRERA_ITV2', 'KM_DARRERA_ITV3', 'KM_DARRERA_ITV4', 'KM_DARRERA_ITV5', 'KW',
               'MARCA', 'MATRICULA', 'MODEL', 'PES_BUIT', 'PES_TOTAL_MÀXIM', 'PES_TOTAL_RODANT', 'TIPUS', 'UNITATS_CO2'}


def register_ingestor_function(path_registre_vehicles: str) -> pd.DataFrame:
    # Load Excel file
    try:
        registre = pd.read_excel(path_registre_vehicles,
                                 header=0,
                                 )
    except:
        raise Exception(f'Not able to ingest Registres Excel File: {path_registre_vehicles}')

    # Check Columns names
    if not COLUMNS_SET.issubset(set(registre.columns)):
        print(f'Nom de columnes diferents, pot donar problemes. Fitxer: {path_registre_vehicles}')
        print(f'Columnes esperades: {COLUMNS_SET}')

    # Parsing of date columns
    registre['DATA_ALTA'] = registre['DATA_ALTA'].apply(date_parser)
    registre['DATA_BAIXA'] = registre['DATA_BAIXA'].apply(date_parser)
    registre['DATA_DARRERA_ITV'] = registre['DATA_DARRERA_ITV'].apply(date_parser)
    registre['DATA_DARRERA_ITV2'] = registre['DATA_DARRERA_ITV2'].apply(date_parser)
    registre['DATA_DARRERA_ITV3'] = registre['DATA_DARRERA_ITV3'].apply(date_parser)
    registre['DATA_DARRERA_ITV4'] = registre['DATA_DARRERA_ITV4'].apply(date_parser)
    registre['DATA_DARRERA_ITV5'] = registre['DATA_DARRERA_ITV5'].apply(date_parser)
    registre['ANY_FABRICACIO'] = registre['ANY_FABRICACIO'].apply(year_of_manufacturing_parser)

    return registre

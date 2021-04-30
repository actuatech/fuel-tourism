import pandas as pd
from .date_parser import date_parser

COLUMNS_SET = set(['ANY_FABRICACIO', 'CARBURANT', 'CARREGA_UTIL', 'CC_CM3', 'CO2', 'CV', 'DATA_ALTA', 'DATA_BAIXA',
               'DATA_DARRERA_ITV', 'DATA_DARRERA_ITV2', 'DATA_DARRERA_ITV3', 'DATA_DARRERA_ITV4', 'DATA_DARRERA_ITV5',
               'KM_DARRERA_ITV', 'KM_DARRERA_ITV2', 'KM_DARRERA_ITV3', 'KM_DARRERA_ITV4', 'KM_DARRERA_ITV5', 'KW',
               'MARCA', 'MATRICULA', 'MODEL', 'PES_BUIT', 'PES_TOTAL_MÀXIM', 'PES_TOTAL_RODANT', 'TIPUS',
                'UNITATS_CO2'])


def register_ingestor_function(path_registre_vehicles) -> pd.DataFrame:

    try:
        registres = pd.read_excel(path_registre_vehicles, header=0)
    except:
        raise Exception(f'Not able to ingest Registres Excel File: {path_registre_vehicles}')

    # Check Columns names
    if not COLUMNS_SET.issubset(set(registres.columns)):
        print(f'Nom de columnes diferents, pot donar problemes. Fitxer: {path_registre_vehicles}')
        print(f'Columnes esperades: {COLUMNS_SET}')

    # Parsing of date columns
    registres['DATA_ALTA'] = registres['DATA_ALTA'].apply(date_parser)
    registres['DATA_BAIXA'] = registres['DATA_BAIXA'].apply(date_parser)

    return registres
